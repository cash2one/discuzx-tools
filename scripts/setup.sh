#!/usr/bin/env bash

sudo apt-get install -y coreutils

# Pip安装Python包的依赖项
sudo apt-get install -y python-dev python-mysqldb
sudo apt-get install -y libmysqlclient-dev libxslt1-dev

# mongodb数据临时存储
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-disthro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# redis数据缓存
if [ ! -d "/opt/program" ]; then
  mkdir -p /opt/program
fi

cd /opt/Program
sudo wget http://download.redis.io/releases/redis-3.2.6.tar.gz
sudo tar xzf redis-3.2.6.tar.gz
cd redis-3.2.6
sudo make

# 安装mp3支持包
sudo sh install-avbin-linux-x86-64-v10

# 安装python环境管理
sudo apt-get install -y python-pip
pip install virtualenv virtualenvwrapper
