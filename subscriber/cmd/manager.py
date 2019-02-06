
from uuid import uuid4
import threading
import time

from luxon.utils.system import execute
from luxon import register
from luxon import db
from luxon.helpers.rmq import rmq
from luxon import g
from luxon.utils.sql import build_where
from luxon.exceptions import SQLIntegrityError
from pyipcalc import IPNetwork

from luxon import GetLogger

log = GetLogger(__name__)


def action(ch, method, properties, msg):
    with db() as conn:
        if msg['type'] == 'append_pool':
            name = msg['pool']['name']
            prefix = msg['pool']['prefix']
            domain = msg['pool']['domain']
            for ip in IPNetwork(prefix):
                try:
                    conn.execute('INSERT INTO tradius_ippool' +
                                 ' (id, domain, pool_name, framedipaddress' +
                                 ', nasipaddress, username, pool_key)' +
                                 ' VALUES' +
                                 " (%s, %s, %s, %s, '', '', '')",
                                 (str(uuid4()), domain, name, ip.first(),))
                    conn.commit()
                except SQLIntegrityError as e:
                    log.warning(e)
        elif msg['type'] == 'delete_pool':
            name = msg['pool']['name']
            prefix = msg['pool']['prefix']
            domain = msg['pool']['domain']
            if prefix is None:
                where = {'pool_name': name,
                         'domain': domain}
                where, values = build_where(**where)
                sql = ('DELETE FROM tradius_ippool' +
                       ' WHERE ')
                sql += where
                conn.execute(sql, values)
                conn.commit()
            else:
                for ip in IPNetwork(prefix):
                    where = {'pool_name': name,
                             'domain': domain,
                             'framedipaddress': ip.first()}
                    where, values = build_where(**where)
                    sql = ('DELETE FROM tradius_ippool' +
                           ' WHERE ')
                    sql += where
                    conn.execute(sql, values)
                    conn.commit()

        elif msg['type'] == 'disconnect':
            nas_ip = msg['session'].get('NAS-IP-Address')
            result = conn.execute("SELECT * FROM tradius_nas" +
                                  " WHERE server = %s",
                                  nas_ip).fetchone()
            if result:
                secret_file = '%s/secret.tmp' % g.app.path
                packet_file = '%s/packet.tmp' % g.app.path

                with open('%s/secret.tmp' % g.app.path, 'w') as f:
                    secret = result['secret']
                    f.write(secret)

                with open('%s/packet.tmp' % g.app.path, 'w') as f:
                    for avp in msg['session']:
                        f.write('%s = "%s"\n' % (avp, msg['session'][avp],))

                if msg['type'] == 'disconnect':
                    execute(['radclient',
                             '-x', '%s:3799' % nas_ip,
                             'disconnect', '-f',
                             packet_file, '-S', secret_file],
                            check=False)


def coa_thread():
    with rmq() as mb:
        mb.receiver('subscriber', action)


def prune_thread():

    with db() as conn:
        while True:
            try:
                conn.execute('DELETE FROM tradius_accounting' +
                             ' WHERE acctstarttime < NOW() - INTERVAL 7 DAY' +
                             ' AND acctstoptime is NULL')
                conn.commit()
            except Exception as e:
                log.warning(e)
            time.sleep(60)


@register.resource('radius', '/manager')
def manager(req, resp):
    # Create new threads
    try:
        threads = []

        threads.append(threading.Thread(target=coa_thread))
        threads.append(threading.Thread(target=prune_thread))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        for thread in threads:
            thread.join()
