#!/usr/bin/env bash

sudo apt-get install libxslt1-dev
sudo apt-get python-dev python-mysqldb

virtual_path="/home/kylin/MyEnvs/kydjango/bin/"

${virtual_path}pip install -r requirements.txt
${virtual_path}python manage.py collectstatic
