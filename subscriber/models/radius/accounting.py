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


@register.model()
class tradius_accounting(SQLModel):
    id = SQLModel.Uuid(default=uuid4, internal=True)
    acctsessionid = SQLModel.String(max_length=64, null=False, default='')
    acctuniqueid = SQLModel.String(max_length=32, null=False, default='')
    username = SQLModel.String(max_length=64, null=False, default='')
    realm = SQLModel.String(max_length=64, null=True, default='')
    nasipaddress = SQLModel.String(max_length=15, null=False, default='')
    nasportid = SQLModel.String(max_length=15, null=True, default=None)
    nasporttype = SQLModel.String(max_length=32, null=True, default=None)
    acctstarttime = SQLModel.DateTime()
    acctupdatetime = SQLModel.DateTime()
    acctstoptime = SQLModel.DateTime()
    acctinterval = SQLModel.Integer(null=True, default=None)
    acctsessiontime = SQLModel.Integer(signed=False, null=True,
                                       default=None)
    acctauthentic = SQLModel.String(null=True, default=None, max_length=32)
    connectinfo_start = SQLModel.String(max_length=50, null=True,
                                        default=None)
    connectinfo_stop = SQLModel.String(max_length=50, null=True, default=None)
    acctinputoctets = SQLModel.BigInt(null=True, default=None)
    acctoutputoctets = SQLModel.BigInt(null=True, default=None)
    calledstationid = SQLModel.String(max_length=50, null=False, default='')
    callingstationid = SQLModel.String(max_length=50, null=False, default='')
    acctterminatecause = SQLModel.String(max_length=32, null=False, default='')
    servicetype = SQLModel.String(max_length=32, default=None, null=True)
    framedprotocol = SQLModel.String(max_length=32, default=None, null=True)
    framedipaddress = SQLModel.String(max_length=15, default='', null=False)
    primary_key = id
    acctuniqueid_index = SQLModel.UniqueIndex(acctuniqueid)
    username_index = SQLModel.Index(username, nasipaddress)
    framedipaddress_index = SQLModel.Index(framedipaddress, nasipaddress)
    acctsessionid_index = SQLModel.Index(acctsessionid)
    acctsessiontime_index = SQLModel.Index(acctsessiontime)
    acctstarttime_index = SQLModel.Index(acctstarttime)
    acctinterval_index = SQLModel.Index(acctinterval)
    acctstoptime_index = SQLModel.Index(acctstoptime)
    nasipaddress_index = SQLModel.Index(nasipaddress)
