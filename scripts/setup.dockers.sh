#!/usr/bin/env bash

sudo apt-get install coreutils

# Pip安装Python包的依赖项
sudo apt-get install libmysqlclient-dev
sudo apt-get install libxslt1-dev
sudo apt-get install python-dev

sudo apt-get redis-server

# 安装mp3支持包
sudo sh install-avbin-linux-x86-64-v10
