import threading,datetime,os,paramiko,tarfile
from scp import SCPClient

def make_tar(fname):
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(fname):
        print(root, dir, files)
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath)
    t.close()

def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs)

def get_ssh(ip,port,user,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = ip, username = user, password = password, port = int(port))
    return ssh

def ssh_scp_put(ssh,local_file,remote_file):
    scp = SCPClient(ssh.get_transport())
    scp.put(local_file,remote_file)
    scp.close()

def upload(ip,port,user,password,local_dir,remote_dir):
    try:
        t=paramiko.Transport((ip,port))
        t.connect(username=user,password=password)
        sftp=paramiko.SFTPClient.from_transport(t)
        print('upload file start %s ' % datetime.datetime.now())
        for root,dirs,files in os.walk(local_dir):
            for filespath in files:
                local_file = os.path.join(root,filespath)
                a = local_file.replace(local_dir,'')
                remote_file = os.path.join(remote_dir,a)
                try:
                    sftp.put(local_file,remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file,remote_file)
                print("upload %s to remote %s" % (local_file,remote_file))
            for name in dirs:
                local_path = os.path.join(root,name)
                a = local_path.replace(local_dir,'')
                remote_path = os.path.join(remote_dir,a)
                try:
                    sftp.mkdir(remote_path)
                    print("mkdir path %s" % remote_path)
                except Exception as e:
                    print(e)
        print('upload file success %s ' % datetime.datetime.now())
        t.close()
    except Exception as e:
        print(e)

def my_run(ip,port,user,password):
    ssh = get_ssh(ip,port,user,password)
    # ssh.exec_command("echo 'export ICP_CI=/usr1/linux_buildcloud-agent'  >> /etc/profile")
    # ssh.exec_command("echo 'export LCRP_HOME=/usr1/LCRP_HOME'  >> /etc/profile")
    # ssh.exec_command("echo 'export PATH=$LCRP_HOME/bin:$PATH'  >> /etc/profile")
    # ssh.exec_command("source /etc/profile")
    #stdin, stdout, stderr = ssh.exec_command("grep -E \"ICP_CI|LCRP_HOME\"  /etc/profile")
    #stdin, stdout, stderr = ssh.exec_command("ls -l /usr1/linux_buildcloud-agent")
    #stdin, stdout, stderr = ssh.exec_command("ls -l /tmp/")
    #stdin, stdout, stderr = ssh.exec_command("rm -rf /tmp/*")
    upload(ip, port, user, password, 'plugins', '/tmp/')
    stdin, stdout, stderr = ssh.exec_command("ls -l /tmp/")
    print(ip,'start put')
    #upload(ip,port,user,password,'plugins','/tmp/')
    print(stdout.read().decode())
    #ssh_scp_put(ssh , 'plugins.tar.gz', '/usr1/linux_buildcloud-agent/')
    #ssh_scp_put(ssh, 'plugins.tar.gz', '/tmp/')
    #print(ip, 'stop put')
    #stdin, stdout, stderr = ssh.exec_command("tar -zxvf /usr1/linux_buildcloud-agent/plugins.tar.gz -C /usr1/linux_buildcloud-agent/")
    #stdin, stdout, stderr = ssh.exec_command("ls -l /usr1/linux_buildcloud-agent/")
    #print(stdout.read().decode())
    # 关闭连接
    ssh.close()
"""
def my_run(ip,port,user,password):
    ssh = get_ssh(ip,port,user,password)
    stdin, stdout, stderr = ssh.exec_command("ls -l /usr1/linux_buildcloud-agent/plugins")
    print(ip,stdout.read().decode())
    # 关闭连接
    ssh.close()
"""
servers_3 = [
        ['10.184.61.231     ', 'huawei'],
        ['10.184.59.108     ', 'huawei'],
        ['10.184.47.220     ', 'huawei'],
        ['10.184.47.228     ', 'huawei'],
        ['10.184.68.235     ', 'huawei'],
        ['10.184.67.61      ', 'huawei'],
        ['10.184.198.230    ', 'huawei'],
        ['10.184.59.81      ', 'huawei'],
        ['10.184.199.240    ', 'huawei'],
        ['10.184.61.158     ', 'huawei'],
        ['10.177.232.254    ', 'huawei'],
        ['10.184.51.29      ', 'EulerOS_123'],
        ['10.184.199.235    ', 'huawei'],
        ['10.184.63.41      ', 'huawei'],
        ['10.184.65.238     ', 'huawei'],
        ['10.184.59.98      ', 'huawei'],
        ['10.184.58.132     ', 'huawei'],
        ['10.184.60.178     ', 'huawei'],
        ['10.184.63.99      ', 'huawei'],
        ['10.184.59.234     ', 'huawei'],
        ['10.184.67.50      ', 'huawei'],
        ['10.184.41.11      ', 'huawei'],
        ['10.184.50.208     ', 'EulerOS_123'],
        ['10.184.198.254    ', 'huawei'],
        ['10.184.60.147     ', 'huawei'],
        ['10.184.59.207     ', 'huawei'],
        ['10.184.199.42     ', 'huawei'],
        ['10.184.59.176     ', 'huawei']
    ]
servers_2=[
    ['10.184.51.150      ', 'EulerOS_123'],
    ['10.184.51.205      ', 'EulerOS_123'],
    ['10.184.50.148      ', 'EulerOS_123'],
    ['10.177.233.13      ', 'huawei'],
    ['10.177.121.234     ', 'EulerOS_123'],
    ['10.184.61.210      ', 'huawei']
]
servers_5=[
    ['10.184.51.221      ', 'EulerOS_123'],
    ['10.184.50.180      ', 'EulerOS_123'],
    ['10.184.49.94       ', 'EulerOS_123'],
    ['10.184.48.185      ', 'EulerOS_123'],
    ['10.184.51.250      ', 'EulerOS_123'],
    ['10.184.48.152      ', 'EulerOS_123'],
    ['10.184.43.180      ', 'EulerOS_123'],
    ['10.184.50.146      ', 'EulerOS_123'],
    ['10.184.159.213     ', 'EulerOS_123'],
    ['10.184.49.144      ', 'EulerOS_123'],
    ['10.184.51.141      ', 'EulerOS_123'],
    ['10.184.152.169     ', 'EulerOS_123'],
    ['10.184.154.126     ', 'EulerOS_123'],
    ['10.184.41.228      ', 'EulerOS_123'],
    ['10.184.46.239      ', 'EulerOS_123'],
    ['10.184.49.253      ', 'EulerOS_123']
]
test=['10.184.152.147      ', 'EulerOS_123']
servers=servers_2


if __name__ == '__main__':
    # make_tar("plugins")
    for server in servers:
        my_run(server[0].strip(),22,'root', server[1].strip())
