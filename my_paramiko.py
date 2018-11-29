#!/usr/bin/python
# -*- coding: utf-8 -*-

#上传文件到远程服务器
import paramiko,datetime,os
hostname = '10.1.101.186'
username = 'root'
password = '123456'
port = 22
local_dir = '/root/paramiko'
remote_dir = '/root/paramiko'
try:
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        files = os.listdir(local_dir)
        for f in files:
                sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f))
        t.close()
except Exception:
        print "connect error!"
#从远程服务器下载文件
import paramiko,datetime,os
hostname = '10.1.101.186'
username = 'root'
password = '123456'
port = 22
local_dir = '/root/paramiko/temp187'
remote_dir = '/root/paramiko/temp186'
try:
        t=paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        files = sftp.listdir(remote_dir) #这里需要注意，列出远程文件必须使用sftp，而不能用os
        for f in files:
                sftp.get(os.path.join(remote_dir,f),os.path.join(local_dir,f))
        t.close()
except Exception:
        print "connect error!"
#执行命令测试
import paramiko
hostname = '10.1.101.186'
username = 'root'
password = '123456'
port = 22

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname,port=port,username=username,password=password)
stdin, stdout, stderr = ssh.exec_command("cd  /root/paramiko;mkdir lxy")
print stdout.readlines()
ssh.close()




import paramiko
#创建SSHClient 实例对象
ssh=paramiko.SSHClient()
#调用方法，表示没有存储远程机器的公钥，允许访问
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接远程机器，地址，端口，用户名密码
ssh.connect('192.168.199.236',22,'root','111111')
#创建目录；
cmd = 'mkdir jcy2'
ssh.exec_command(cmd)
#如果命令行跨行
cmd='''echo '123
45678
90abc'
 >myfile'''
ssh.exec_command(cmd)
#获取命令行的执行结果
cmd ='cat myfile'
stdin,stdout,stderr =ssh.exec_command(cmd)
print(stdout.read()+stderr.read())
ssh.close()

        注意点：
        exec_command每次执行都会打开一个新的channel，执行；
        2.新的环境，不再上次执行的环境里面
        3.所以我们不能多次调用，达到多次执行的目的

例如：如下代码：

ssh.exec_command('pwd')
ssh.exec_command('mkdir jcy3')
ssh.exec_command('cd jcy3')
stdin,stdout,stderr =ssh.exec_command('pwd')

print(stdout.read())
ssh.close()

linux 命令：free查看内存信息；
我们以后可以在代码里面每隔5分钟，看一下内存的情况；

        如下是传输文件到远程：

import paramiko
#创建SSHClient 实例对象
ssh=paramiko.SSHClient()
#调用方法，表示没有存储远程机器的公钥，允许访问
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#连接远程机器，地址，端口，用户名密码
ssh.connect('192.168.199.236',22,'root','111111')
sftp=ssh.open_sftp()
sftp.put('ftp1.py','home/stt/ftp1.py')
sftp.close()
