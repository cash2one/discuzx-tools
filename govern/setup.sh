#!/usr/bin/env bash

sudo mkdir -p media

sudo apt-get install -y libxslt1-dev python-dev python-mysqldb

sudo wget https://github.com/libevent/libevent/releases/download/release-2.0.22-stable/libevent-2.0.22-stable.tar.gz
sudo tar xzf libevent-2.0.22-stable.tar.gz
cd libevent-2.0.22-stable
sudo ./configure
sudo make
sudo make install

sudo rm libevent-2.0.22-stable.tar.gz
sudo rm -R libevent-2.0.22-stable

sudo apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev
sudo apt-get install -y liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk

env=$1
if [ "$env" = "remote" ]; then
    virtual_path="/opt/Program/pyenvs/quant_admin/bin/"
else
    virtual_path="/home/kylin/Program/pyenvs/quant_admin/bin/"
fi

${virtual_path}pip install -r requirements.txt
${virtual_path}python manage.py collectstatic
