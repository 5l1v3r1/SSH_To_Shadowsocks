#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssh_login

if __name__ == '__main__':
    input = input('1(ss部署) or 0(下载文件):\n')
    ssh_login.LoginSsh(int(input))