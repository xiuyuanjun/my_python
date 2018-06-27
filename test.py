
from pyhive import hive
conn = hive.Connection(host='192.168.1.181', port=22, username='xiuyuanjun', database='default')
conn.execute('select * from url_log limit 10')
for result in conn.fetchall():
    print(result)