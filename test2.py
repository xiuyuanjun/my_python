#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

# 将要部署的服务器信息通过命令行参数的形式传入
hostname = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]
frompath = sys.argv[5]
topath = sys.argv[6]
workspace = sys.argv[7]


class ShellHandler(object):
    def __init__(self, hostname, username, password, port):
        import paramiko
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
        from scp import SCPClient
        scp = SCPClient(self.ssh.get_transport())
        scp.put(frompath, topath)
        scp.close()

    def deploy(self, frompath, topath, workspace, deploy_script, pre_cmd):
        self.execute(pre_cmd)
        self.send_file(frompath, topath)


def main():
    import threading
    # 预处理环境，清理上一次部署遗留的文件
    pre_cmd = "rm -f " + topath + "/*.tar.gz"
    deploy_script = '/deploy_eums.sh'
    # 因为hostname可能是一个包含多个机器的字符串，所以需要对其进行分割处理
    ip_list = hostname.split(',')
    threads = []  # 运行的线程列表
    for ip in ip_list:
        t = threading.Thread(target=ShellHandler(ip, username, password, port).deploy,
                             args=(frompath, topath, workspace, deploy_script, pre_cmd))
        threads.append(t)  # 将子线程追加到线程列表
    for t in threads:
        t.start()
        t.join()
    print("DEPLOYMENT SUCCESS!")


if __name__ == "__main__":
    main()