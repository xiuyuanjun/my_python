#!/usr/bin/python3

import pymysql
import os
import tarfile
import time

class ShellHandler(object):
    def __init__(self, hostname, username, password, port):
        import paramiko
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = hostname, username = username, password = password, port = int(port))
        channel = self.ssh.invoke_shell()
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

    def __del__(self):
        self.ssh.close()

    def execute(self, cmd):
        import re
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()

        shout = []
        sherr = []
        exit_status = 0
        for line in self.stdout:
            if str(line).startswith(cmd) or str(line).startswith(echo_cmd):
                # up for now filled with shell junk from stdin
                shout = []
            elif str(line).startswith(finish):
                # our finish command ends with the exit status
                exit_status = int(str(line).rsplit(maxsplit=1)[1])
                if exit_status:
                    # stderr is combined with stdout.
                    # thus, swap sherr with shout in a case of failure.
                    sherr = shout
                    shout = []
                break
            else:
                # get rid of 'coloring and formatting' special characters
                shout.append(re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]').sub('', line).
                             replace('\b', '').replace('\r', ''))

        # first and last lines of shout/sherr contain a prompt
        if shout and echo_cmd in shout[-1]:
            shout.pop()
        if shout and cmd in shout[0]:
            shout.pop(0)
        if sherr and echo_cmd in sherr[-1]:
            sherr.pop()
        if sherr and cmd in sherr[0]:
            sherr.pop(0)
        return shin, shout, sherr

    def send_file(self, frompath, topath):
        from scp import SCPClient
        scp = SCPClient(self.ssh.get_transport())
        scp.put(frompath, topath)
        scp.close()

    def deploy(self,frompath,topath,workspace,deploy_script,pre_cmd,deploy_cmd):
        self.execute(pre_cmd)
        self.send_file(frompath, topath)
        self.send_file(workspace + deploy_script, topath)
        self.execute(deploy_cmd)

'''
    python中的tarfile模块实现文档的归档压缩和解压缩

    功能：
        把工作空间下面的所有文件，打包生成一个tar文件
        同时提供一个方法把该tar文件中的一些文件解压缩到
        指定的目录中
'''
# global var
SHOW_LOG = True
# tar文件存放位置
TAR_PATH = ''
# 取出文件存放目录
EXT_PATH = ''
def write_tar_file(path, content):
    '''打开指定path的tar格式的文件，如果该文件不存在
    系统会自动创建该文件，如果该文件以及存在，则打开文件
    打开文件后，向文件中添加文件(这个功能类似于把几个文件
    打包成tar包文件)'''
    with tarfile.open(path, 'w') as tar:
        if SHOW_LOG:
            print('打开文件:[{}]'.format(path))
        for n in content:
            if SHOW_LOG:
                print('压缩文件:[{}]'.format(n))
            tar.add(n)
        if SHOW_LOG:
            print('关闭文件[{}]'.format(path))
        tar.close()


def get_workspace_files():
    '''获取工作空间下面的所有文件，然后以列表的形式返回'''
    if SHOW_LOG:
        print('获取工作空间下的所有文件...')
    #只需要归档mysql目录即可
    return ['mysql']


def extract_files(tar_path, ext_path, ext_name):
    '''解压tar文件中的部分文件到指定目录中'''
    with tarfile.open(tar_path) as tar:
        if SHOW_LOG:
            print('打开文件:[{}]'.format(tar_path))
        names = tar.getnames()
        if SHOW_LOG:
            print('获取到所有文件名称:{}'.format(names))
        for name in names:
            if name.split('.')[-1] == ext_name:
                if SHOW_LOG:
                    print('提取文件：[{}]'.format(name))
                tar.extract(name, path=ext_path)


def mkdir(path):
    '''创建不存在的目录'''
    if os.path.exists(path):
        if SHOW_LOG:
            print('存在目录:[{}]'.format(path))
    else:
        if SHOW_LOG:
            print('创建目录:[{}]'.format(path))
        os.mkdir(path)


def init():
    global SHOW_LOG
    SHOW_LOG = True
    # tar文件存放位置
    global TAR_PATH
    TAR_PATH = '/home/mysql.tar'
    # 取出文件存放目录
    global EXT_PATH
    EXT_PATH = '/tmp/temp/'
    # 创建目录，如果目录不存在
    path = os.path.split(TAR_PATH)[0]
    mkdir(path)
    mkdir(EXT_PATH)


def main():
    #暂停八小时再执行
    for i in range(8*60*60):
        print("暂停第%s秒"%i)
        time.sleep(1)
    # 打开数据库连接
    db = pymysql.connect(host="192.168.1.187", port=53306, user="root", passwd="123456", db='mysql', charset='utf8')
    cursor = db.cursor()
    # 锁表操作
    cursor.execute("FLUSH TABLES WITH READ LOCK")
    cursor.execute("SHOW MASTER STATUS")
    data = cursor.fetchall()
    print(data)

    init()
    content = get_workspace_files()
    # 打包文件
    write_tar_file(TAR_PATH, content)
    print('#' * 50)
    # 提取文件
    #extract_files(TAR_PATH, EXT_PATH, 'html')
    #传送文件
    shell = ShellHandler('192.168.1.187', 'root', 'Kj@xa#dsj!23', 22)
    shell.send_file('/home/mysql.tar','/home/zhaoxueqing/')

    #再次查看主库状态
    cursor.execute("SHOW MASTER STATUS")
    db.commit()
    #关闭数据库连接
    db.close()
main()
