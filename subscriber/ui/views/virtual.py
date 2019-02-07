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
from luxon import g
from luxon import router
from luxon import register
from luxon import render_template
from luxon.utils.bootstrap4 import form

from subscriber.ui.models.radius.virtual import tradius_virtual

g.nav_menu.add('/Infrastructure/Radius/Virtual',
               href='/infrastructure/radius/virtual',
               tag='infrastructure:admin',
               feather='at-sign')


@register.resources()
class Virtual():
    def __init__(self):
        router.add('GET',
                   '/infrastructure/radius/virtual',
                   self.list,
                   tag='infrastructure:admin')

        router.add('GET',
                   '/infrastructure/radius/virtual/{id}',
                   self.view,
                   tag='infrastructure:admin')

        router.add('GET',
                   '/infrastructure/radius/virtual/delete/{id}',
                   self.delete,
                   tag='infrastructure:admin')

        router.add(('GET', 'POST',),
                   '/infrastructure/radius/virtual/add',
                   self.add,
                   tag='infrastructure:admin')

        router.add(('GET', 'POST',),
                   '/infrastructure/radius/virtual/edit/{id}',
                   self.edit,
                   tag='infrastructure:admin')

        router.add('POST',
                   '/infrastructure/radius/virtual/add_nas/{id}',
                   self.add_nas,
                   tag='infrastructure:admin')

        router.add('GET',
                   '/infrastructure/radius/virtual/rm_nas/{id}',
                   self.rm_nas,
                   tag='infrastructure:admin')

        router.add('GET',
                   '/infrastructure/radius/virtual/clear/{id}',
                   self.clear,
                   tag='infrastructure:admin')

    def list(self, req, resp):
        return render_template('tradius.ui/virtual/list.html',
                               view='Virtual Authentication Sevices')

    def delete(self, req, resp, id):
        req.context.api.execute('DELETE', '/v1/virtual/%s' % id,
                                endpoint='radius')

    def view(self, req, resp, id):
        vr = req.context.api.execute('GET', '/v1/virtual/%s' % id,
                                     endpoint='radius')
        html_form = form(tradius_virtual, vr.json, readonly=True)
        return render_template('tradius.ui/virtual/view.html',
                               view='View Virtual Authentication Service',
                               form=html_form,
                               id=id)

    def edit(self, req, resp, id):
        if req.method == 'POST':
            req.context.api.execute('PUT', '/v1/virtual/%s' % id,
                                    data=req.form_dict,
                                    endpoint='radius')
            return self.view(req, resp, id)
        else:
            domain = req.context.api.execute('GET', '/v1/virtual/%s' % id,
                                             endpoint='radius')
            html_form = form(tradius_virtual, domain.json)
            return render_template('tradius.ui/virtual/edit.html',
                                   view='Edit Virtual Authentication Service',
                                   form=html_form,
                                   id=id)

    def add(self, req, resp):
        if req.method == 'POST':
            response = req.context.api.execute('POST', '/v1/virtual',
                                               data=req.form_dict,
                                               endpoint='radius')
            return self.view(req, resp, response.json['id'])
        else:
            html_form = form(tradius_virtual)
            return render_template('tradius.ui/virtual/add.html',
                                   view='Add Virtual Authentication Service',
                                   form=html_form)

    def add_nas(self, req, resp, id):
        data = req.form_dict

        uri = '/v1/virtual/%s/nas' % id

        response = req.context.api.execute('POST', uri, data=data,
                                           endpoint='radius')

    def rm_nas(self, req, resp, id):
        uri = '/v1/virtual/%s/nas' % id
        response = req.context.api.execute('DELETE', uri, endpoint='radius')  

    def clear(self, req, resp, id):
        uri = '/v1/clear/%s' % id
        response = req.context.api.execute('PUT', uri, endpoint='radius')  
