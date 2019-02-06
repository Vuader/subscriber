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
from uuid import uuid4

from luxon import register
from luxon import SQLModel

from subscriber.models.radius.pool import tradius_pool


@register.model()
class tradius_ippool(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    domain = SQLModel.Fqdn(internal=True)
    pool_name = SQLModel.String(max_length=30, null=False)
    framedipaddress = SQLModel.String(max_length=15, default='', null=False)
    nasipaddress = SQLModel.String(max_length=15, null=False, default='')
    calledstationid = SQLModel.String(max_length=30, null=True)
    callingstationid = SQLModel.String(max_length=30, null=True)
    expiry_time = SQLModel.DateTime(null=True, default=None)
    username = SQLModel.String(max_length=64, default='', null=False)
    pool_key = SQLModel.String(max_length=30, null=False)
    primary_key = id
    poolname_expire_index = SQLModel.Index(pool_name, expiry_time)
    framedipaddress_index = SQLModel.Index(framedipaddress)
    nasip_poolkey_ipaddress_index = SQLModel.Index(nasipaddress, pool_key,
                                                   framedipaddress)
    unique_pool_ip = SQLModel.UniqueIndex(pool_name, framedipaddress)
    pool_name_ref = SQLModel.ForeignKey(pool_name, tradius_pool.pool_name)
