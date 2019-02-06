
from luxon.utils.pkg import Module
from luxon.utils.files import rm
from luxon import register


@register.resource('radius', '/setup')
def setup(req, resp):
    module = Module('subscriber')
    rm('/etc/freeradius/3.0', recursive=True)
    module.copy('freeradius', '/etc/freeradius/3.0')
