## 概述
    Discuz自动上传附件，发帖，注册用户，留言，顶帖等自动化工具。

## 文件结构:
    公共方法
    common:
        func.py
        common.py        
        logger.py

    配置项
    conf:
        control.py
        data_config.py
        logger_config.py
        store_config.py
        supervisor_app.conf
        supervisor_dev.conf
        web_config.conf

    启动脚本项
    scripts:
        mongo.bat
        mongo.sh
        app_supervisorctl.sh
        dev_supervisorctl.sh

    数据模型
    models:
        base.py
        record.py
        remote.py

    上传文件
    upload:
        __init__.py
        common.py
        config.py
        demo.py
        main.py
        measure.py
        README.md
    
    下载文件
    web:

    注册用户
    register:
    
    动发帖
    posting:

    .gitignore
    readme.md
    requirements.txt
