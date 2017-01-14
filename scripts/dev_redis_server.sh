#!/usr/bin/env bash

if [ ! -d "/var/log/redis/" ]; then
    sudo mkdir -pv /var/log/redis/
fi

sudo redis-server ../deploy/redis_server.conf
