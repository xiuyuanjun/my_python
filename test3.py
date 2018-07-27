#!/usr/bin/env python
import paramiko
from scp import SCPClient

class ShellHandler(object):
    def __init__(self, hostname, username, password, port):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname, username=username, password=password, port=int(port))
        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def execute(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdin, stdout, stderr

    def send_file(self, frompath, topath):
        scp = SCPClient(self.ssh.get_transport())
        scp.put(frompath, topath)
        scp.close()

def main():
    ssh = ShellHandler(hostname='10.10.1.181',username='xiuyuanjun',password='123456',port=22)

    sql = "hive -e \"select distinct a.dest_number from zx_base_mt a where a.scan_start_time >= '2018-01-01' and a.dest_number not in (select b.dest_number from zx_already_send_number b union all select c.phone_number dest_number from pre_white c ) limit  4000000;\""
    #sql = "hive -e \"select * from sms_mt limit 100\""
    print(sql)
    stdin, stdout, stderr = ssh.execute(sql)
    list_stdout = [line for line in list(stdout) if 'WARN' not in line]
    outer = [list_stdout[n:n+200000] for n in range(0,len(list_stdout),200000)]
    for n,lines in enumerate(outer):
        file = open('zhangxue_{index}.txt'.format(index=n), 'a')
        for line in lines:
            file.write(line)
        file.close()
    for number in list_stdout:
        insert_sql = "hive -e \"insert into zx_already_send_number values ({dest_number}, '', '', 'game', '2018-07-26')\"".format(dest_number=number)
        ssh.execute(insert_sql)
if __name__ == '__main__':
    main()