#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
支持python2和python3
依赖库:os
服务器自动配置脚本
@author:huha
'''
import os
def run():
    '''
    下载shadowsocks，服务器后台启动ss
    :return: 信息列表
    '''
    results = []
    cmd = "git clone -b master https://github.com/shadowsocks/shadowsocks.git"
    result=os.popen(cmd).read()
    results.append(result)
    results.append("-"*50+"\n开始ss简易部署"+'-'*10)
    # 关闭服务端后台已配置的ss代理
    cmd = "python shadowsocks/shadowsocks/server.py -c config.json -d stop"
    if "stop" in os.popen(cmd).read():
        result = "检测到已存在ss服务，重新部署ss"
    results.append(result)
    cmd = "python shadowsocks/shadowsocks/server.py -c config.json -d start"
    result=os.popen(cmd).read()
    results.append(result)
    return results

if __name__ == '__main__':
    print('-'*50)
    for info in run():
        if info:
            print(info)
    print("ss部署成功\n"+'-'*50)