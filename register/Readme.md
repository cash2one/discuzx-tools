## 介绍:
    生成测试数据, 用于内容的充实和支撑.
    适配业务规则, 上线如果需要, 以服务的形式运行, 来模拟用户操作, 产生优质内容.

## 使用:
    第一, 启动Mongodb 服务
    第二, 参看config.py 配置项设置
    第三, 导入基础数据 pyhton mongo.py
    第四, 运行 nohup python fakery.py >> fakery.log &

## mongodb:

    sudo service mongod start
    sudo service mongod stop
    sudo service mongod restart
    where <port> is the port configured in /etc/mongod.conf, 27017 by default.

## 脚本:
    db.<collection>.find({id:33})
    db.<collection>.find().sort({ id : 1 })
