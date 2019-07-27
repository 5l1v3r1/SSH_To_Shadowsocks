# SSH_To_Shadowsocks
SSH远程一键部署shadowsocks代理脚本

* 使用环境centos,其他环境待测
* 通过SSH上传服务器需要的ss配置文件，执行服务器系统命令配置ss
* 支持多线程同时配置多台服务器
* config.json文件path字段设置下载文件目录

# config.json格式
* 其中config字段为ss配置文件，具体参照这里
https://github.com/shadowsocks/shadowsocks/wiki/Configuration-via-Config-File
```buildoutcfg
[
    {
        "config":{
            "fast_open":false,
            "local_address":"127.0.0.1",
            "local_port":"1080",
            "method":"aes-256-cfb",
            "port_password":{
                "1234":"1234"
            },
            "server":"0.0.0.0",
            "timeout":300
        },
        "ip":"服务器IP1",
        "password":"密码",
        "username":"用户名",
        "path": "下载文件目录"
    }
    {
        "config":{
            "fast_open":false,
            "local_address":"127.0.0.1",
            "local_port":"1080",
            "method":"aes-256-cfb",
            "port_password":{
                "1234":"1234"
            },
            "server":"0.0.0.0",
            "timeout":300
        },
        "ip":"服务器IP2",
        "password":"密码",
        "username":"用户名",
        "path": "下载文件目录"
    }
    ...
]

```
