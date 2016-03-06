#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/opt/myenvs/kydiscuzx/bin/supervisorctl -c ${base_path}/conf/supervisor_app.conf
