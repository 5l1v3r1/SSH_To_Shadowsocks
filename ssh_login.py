#!/usr/bin/python
# -*- encoding:utf-8 -*-
'''
远程登陆配置模块,实现远程登陆并上传配置文件
@author:huha
'''

import logging
import json
import threading
import paramiko
import os
from stat import S_ISDIR as isdir


class Sshell:
    logger = logging.getLogger('login_logger')
    def __init__(self, json_str):
        self.config = json_str
        self.ip = self.config['ip']
        self.pw = self.config['password']
        self.username = self.config['username']
        self.path = self.config['path']


    def downfile(self, sftp, local_dir_name, remote_dir_name='/tmp'):
        """
        下载远程服务器文件
        :return:
        """
        remote_file = sftp.stat(remote_dir_name)
        # print(remote_file)
        if isdir(remote_file.st_mode):
            # 文件夹，不能直接下载，需要继续循环
            if not os.path.exists(local_dir_name):
                os.makedirs(local_dir_name)
            print('开始下载文件夹：' + remote_dir_name)
            for remote_file_name in sftp.listdir(remote_dir_name):
                sub_remote = os.path.join(remote_dir_name, remote_file_name)
                sub_remote = sub_remote.replace('\\', '/')
                sub_local = os.path.join(local_dir_name, remote_file_name)
                sub_local = sub_local.replace('\\', '/')
                self.downfile(sftp, sub_local, sub_remote)
        else:
            # 文件，直接下载
            print('开始下载文件：' + remote_dir_name)
            sftp.get(remote_dir_name, local_dir_name)



    def upfile(self,sftp):
        """
        上传配置文件,服务器存放路径：/tmp/server
        :return:
        """
        print("开始上载文件...\nIP:"+self.ip)
        # 上传服务端所需的json文件
        with open('config/config.json', 'w', encoding='utf-8') as file:
            # print(self.config['config'])
            file.write(json.dumps(self.config['config'], indent=2, ensure_ascii=False))
        sftp.put('config/config.json', '/tmp/server/config.json')
        sftp.put('remote_run.py', '/tmp/server/remote_run.py')
        print("文件上载成功...")


    def login(self):
        """
        登陆远程服务器，并创建文件夹
        :return:
        """
        print("登陆远程服务器...\nIP:"+self.ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # print(self.username, self.ip, self.pw)
        try:
           ssh.connect(self.ip, 22, self.username, self.pw, allow_agent=False, look_for_keys=False)
           ssh.exec_command('mkdir /tmp/server')
        except Exception as e:
            # 控制台输出错误信息
            Sshell.logger.warning("\nIP:"+self.ip+"【ERROR】：登陆失败,请检查账户配置=====>>>error: "+str(e)+'\n')
        else:
            print("成功登陆远程服务器\n"+'-'*50)
            return ssh

    def start(self, input):
        """
        部署ss相关环境：git/python
        上传配置文件
        适用服务器操作系统：centos
        :return:
        """
        try:
            self.ssh = self.login()
        except Exception:
            raise Exception
        t = self.ssh.get_transport()
        sftp = paramiko.SFTPClient.from_transport(t)
        if input:
            self.upfile(sftp)
            print('-'*50)
            stdin, stdout, stderr = self.ssh.exec_command("yum install -y python git")
            if stderr:
                Sshell.logger.warning(stderr.read().decode('utf-8'))
                print(stdout.read().decode('utf-8'))
            print(stdout.read().decode('utf-8'))
            stdin, stdout, stderr = self.ssh.exec_command("cd /tmp/server && python remote_run.py")
            print(stdout.read().decode('utf-8'))
            self.ssh.close()
        else:
            self.downfile(sftp, self.ip+self.path, self.path)


def LoginSsh(input):
    with open('config.json', 'r') as f:
        server_configs = json.loads(f.read())
    print(server_configs)
    # 创建线程列表
    thread_pool = []
    for server_config in server_configs:
        ssh_shell = Sshell(server_config)
        thread_pool.append(threading.Thread(target=ssh_shell.start(input)))
    # 进行多台服务器部署
    for t in thread_pool:
        t.start()
    t.join()