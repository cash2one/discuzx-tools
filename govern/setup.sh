#!/usr/bin/env bash

sudo apt-get install libxslt1-dev
sudo apt-get python-dev python-mysqldb

sudo wget http://jaist.dl.sourceforge.net/project/levent/libevent/libevent-2.0/libevent-2.0.22-stable.tar.gz
sudo tar xzf libevent-2.0.22-stable.tar.gz
cd libevent-2.0.22-stable
sudo make

env=$1
if [ "$env" -eq "remote" ]; then
    virtual_path="/opt/myenvs/kydjango/bin/"
else
    virtual_path="/home/kylin/MyEnvs/kydjango/bin/"
fi

${virtual_path}pip install -r requirements.txt
${virtual_path}python manage.py collectstatic
