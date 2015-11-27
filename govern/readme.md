论坛自动工具数据管理后台

### Kill ProName:
ps -ef | grep govern | grep -v grep | cut -c 9-15 | xargs kill -s 9
