## 概述
    Discuz自动上传附件，发帖，注册用户，留言，顶帖等自动化工具。

# 安装
    1, 安装MySQL.
    2, 执行./script/setup.sh.
    3, 创建python运行虚拟环境, 在虚拟环境执行: pip install -r requirements.txt.

# 介绍
    ./*.py      服务脚本
    ./web       七牛文件下载代理
    ./govern    数据管理后台

# 安全
    注意：账户密码信息的存放，建议对Demo默认值的更改，放置在系统的环境变量中。相关配置信息的数据，分类存放在以下配置文件里：

    ./conf/env_conf.py          # 从环境变量中读取敏感配置信息
    ./conf/data_config.py       # 数据相关配置信息 (MySQL\Redis\MongoDB)
    ./conf/store_conf.py        # 存储相关配置信息
    ./conf/regular_conf.py      # 业务规则配置信息
    
    ./scripts/readme.md         # MongoDb可能使用的DBA账户
    ./govern/govern/settings.py # 管理后台配置信息 (Email\MySQL)

    提醒：./conf/data_config.py 里 Redis\MongoDB 账户或密码的更改，请注意与 ./conf/redis_server.conf 或 ./conf/mongod.conf 一致。
    
# 环境变量设置
    ./env_conf_init.txt 分两部分
