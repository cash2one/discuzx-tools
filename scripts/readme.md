## mongoDb:
    $ mongo --host 127.0.0.1:27027
    
    > use admin
    switched to db admin
    > db.addUser("kylinfish", "hi123456wjg")
    WARNING: The 'addUser' shell helper is DEPRECATED. Please use 'createUser' instead
    Successfully added user: { "user" : "kylinfish", "roles" : [ "root"  ]  }
    
    > use dz_gen_data;
    switched to db dz_gen_data
    > show users;
    > db.addUser('wuuuang','WJGFd9E6IWBWpf0f7HzEb2929b7')
    WARNING: The 'addUser' shell helper is DEPRECATED. Please use 'createUser' instead
    Successfully added user: { "user" : "wuuuang", "roles" : [ "dbOwner"  ]  }
    > exit
    bye

    $mongo 127.0.0.1:27027/admin -u kylinfish -p hi123456wjg
    $mongo 127.0.0.1:27027/dz_gen_data -u wuuuang -p WJGFd9E6IWBWpf0f7HzEb2929b7

## redis-server:
    redis-cli -h 127.0.0.1 -p 6389 -a E8IWB8pf0PfE4F9df2927b9b7
    redis-cli -h 127.0.0.1 -p 6379 keys '*' >> /opt/redis_keys.txt

