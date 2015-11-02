#!/usr/bin/env bash

sudo apt-get install coreutils

# Pip安装Python包的依赖项
sudo apt-get install libmysqlclient-dev
sudo apt-get install libxslt1-dev
sudo apt-get install python-dev

# mongodb数据临时存储
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-disthro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# redis数据缓存
if [ ! -d "/opt/program" ]; then
  mkdir /opt/program
fi

cd /opt/program
sudo wget http://download.redis.io/releases/redis-3.0.5.tar.gz
sudo tar xzf redis-3.0.5.tar.gz
cd redis-3.0.5
sudo make
