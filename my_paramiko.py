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
