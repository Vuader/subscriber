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
from luxon import register
from luxon import router
from luxon.helpers.access import validate_access
from luxon.helpers.api import raw_list, sql_list, obj
from luxon.utils.hashing import md5sum

from subscriber.models.radius.users import tradius_user
from subscriber.models.radius.user_groups import tradius_user_group
from subscriber.models.radius.user_attrs import tradius_user_attr
from subscriber.helpers.radius.groups import get_user_groups
from subscriber.helpers.radius.users import disconnect

from tradius.lib.avps import avps

from luxon import GetLogger

log = GetLogger(__name__)


@register.resources()
class Users(object):
    def __init__(self):
        # Services Users
        router.add('GET', '/v1/user/{id}', self.user,
                   tag='services:view')
        router.add('GET', '/v1/users', self.users,
                   tag='services:view')
        router.add('POST', '/v1/user', self.create,
                   tag='services:admin')
        router.add(['PUT', 'PATCH'], '/v1/user/{id}', self.update,
                   tag='services:admin')
        router.add('DELETE', '/v1/user/{id}', self.delete,
                   tag='services:admin')

        router.add('GET', '/v1/user_attrs/{user_id}', self.attrs,
                   tag='services:view')
        router.add('POST', '/v1/user_attr/{user_id}', self.add_attr,
                   tag='services:admin')
        router.add('DELETE', '/v1/user_attr/{user_id}/{group_id}',
                   self.rm_attr,
                   tag='services:admin')

        router.add('GET', '/v1/user_groups/{user_id}', self.groups,
                   tag='services:view')
        router.add('POST', '/v1/user_group/{user_id}', self.add_group,
                   tag='services:admin')
        router.add('DELETE', '/v1/user_group/{user_id}/{group_id}',
                   self.rm_group,
                   tag='services:admin')

        router.add('GET', '/v1/avps', self.avps,
                   tag='login')

    def user(self, req, resp, id):
        return obj(req, tradius_user, sql_id=id,
                   hide=('password',))

    def users(self, req, resp):
        return sql_list(req, 'tradius_user',
                        ('id', 'username', 'name',),)

    def create(self, req, resp):
        user = obj(req, tradius_user,
                   hide=('password',))
        if req.json.get('password'):
            user['password'] = md5sum(req.json['password'])
        user.commit()
        return user

    def update(self, req, resp, id):
        user = obj(req, tradius_user, sql_id=id,
                   hide=('password',))

        if req.json.get('password'):
            user['password'] = md5sum(req.json['password'])

        if req.json.get('enabled'):
            if user['enabled'] is False:
                disconnect(user['virtual_id'],
                           user['username'])

        user.commit()
        return user

    def delete(self, req, resp, id):
        user = obj(req, tradius_user, sql_id=id)
        disconnect(user['virtual_id'],
                   user['username'])
        user.commit()

    def groups(self, req, resp, user_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        user_groups = get_user_groups(user_id)
        return raw_list(req, user_groups, sql=False)

    def add_group(self, req, resp, user_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        attr = obj(req, tradius_user_group)
        attr['user_id'] = user_id
        attr.commit()

    def rm_group(self, req, resp, user_id, group_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        attr = obj(req, tradius_user_group, sql_id=group_id)
        attr.commit()

    def attrs(self, req, resp, user_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        where = {'user_id': user_id}
        return sql_list(req, 'tradius_user_attr',
                        ('id', 'attribute', 'op', 'value',),
                        where=where)

    def add_attr(self, req, resp, user_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        attr = obj(req, tradius_user_attr)
        attr['user_id'] = user_id
        attr.commit()
        return attr

    def rm_attr(self, req, resp, user_id, group_id):
        user = tradius_user()
        user.sql_id(user_id)
        validate_access(req, user)
        attr = obj(req, tradius_user_attr, sql_id=group_id)
        attr.commit()

    def avps(self, req, resp):
        return raw_list(req, avps)
