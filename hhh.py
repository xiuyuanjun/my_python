import tarfile
import os
import sys
workspace = sys.argv[1]
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
def tar(route):
    os.chdir(route)
    t = tarfile.open("destination.tar.gz", "w:gz")
    for root, dir, files in os.walk('.',True):
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath)
    t.close()
    return 'tar success!'
def search(workspace):
    for root, dirs, files in os.walk(workspace, True):
        if 'destination.tar.gz' in files:
            return os.path.join(root, 'destination.tar.gz')

if __name__ == "__main__":
    deploy_cmd="rm -rf /home/nginx/html/manager/*;tar -zxvf /home/jenkins/spacei-web/destination.tar.gz -C /home/nginx/html/manager/"
    jg = tar('dist')
    print(jg)
    print(search(workspace))
    ssh = ShellHandler(hostname='111.20.252.18',username='jenkins',password='qWeR1234!@#$',port=50022)
    ssh.send_file(search(workspace),'~/spacei-web/')
    ssh.execute(deploy_cmd)
