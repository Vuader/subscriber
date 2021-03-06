# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Christiaan Frans Rademan.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holders nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

from luxon import db
from luxon.helpers.rmq import rmq
from luxon.utils.sql import build_where
from luxon import js 


def pod(acct_id):
    with rmq() as mb:
        with db() as conn:
            result = conn.execute('SELECT * FROM tradius_accounting' +
                                 ' WHERE id = %s', acct_id).fetchall()
            for cdr in result:
                message = {
                    'type': 'disconnect',
                    'session': {'Acct-Session-Id': cdr['acctsessionid'],
                                'User-Name': cdr['username'],
                                'NAS-IP-Address': cdr['nasipaddress']}
                }
                mb.distribute('subscriber', **message)
                conn.execute('UPDATE tradius_accounting' +
                             ' SET acctstoptime = now()' +
                             ' WHERE id = %s', acct_id)
                conn.commit()


def clear(nas_id):
    with db() as conn:
        result = conn.execute('SELECT * FROM tradius_nas' +
                              ' WHERE id = %s', nas_id).fetchone()
        if result:
            server = result['server']
            conn.execute('UPDATE tradius_accounting' +
                         ' SET acctstoptime = now()' +
                         ' WHERE nasipaddress = %s', server)
            conn.commit()
