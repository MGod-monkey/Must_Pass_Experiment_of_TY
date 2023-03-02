#!/bin/bash
echo ">>>正在启动服务器..."
echo ""
cd ./solr/bin
chmod a+x solr
./solr start -force
cd ../../solrproject

# 获取本机地址
ip_address=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | sed -n '2p' | awk '{print $2}')
log_dir="$HOME/log"

if [ ! -d "$log_dir" ]; then
  echo ">>>日志文件夹不存在,正在新建: $log_dir"
  mkdir "$log_dir"
fi

file_path="$HOME/log/run.out"
`nohup python manage.py runserver $ip_address:8000 > $file_path 2>&1 &` ; ls -l >> /dev/null
echo ""
echo ">>>服务器启动完毕！日志见$file_path"