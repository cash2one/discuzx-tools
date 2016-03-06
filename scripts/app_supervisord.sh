#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/opt/myenvs/kydiscuzx/bin/supervisord -c ${base_path}/conf/supervisor_app.conf
