#!/bin/bash

base_path=$(cd `dirname $0`; pwd)
/home/kylin/MyEnvs/kydiscuzx/bin/supervisorctl -c ${base_path}/conf/supervisor_run.conf
