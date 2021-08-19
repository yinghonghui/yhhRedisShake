#!/bin/bash
cd /root 
git clone https://github.com/yinghonghui/yhhRedisShake.git
wget https://golang.google.cn/dl/go1.16.5.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.16.5.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >>~/.bashrc
echo 'export GOPROXY=https://goproxy.cn' >>~/.bashrc
source ~/.bashrc
set GOARCH=amd64
set GOOS=linux
cd /root/yhhRedisShake/src
go build /root/yhhRedisShake/src/redis-shake/main
mv /root/yhhRedisShake/src/main /root/yhhRedisShake/conf/
rm -rf /root/yhhRedisShake/conf/redis-shake.conf
cd /root
chmod -Rf 777 yhhRedisShake/



cd /root/yhhRedisShake/conf
./main -type=sync -conf=/tmp/RedisShake/conf/redis-shake.conf

./root/yhhRedisShake/conf/main -type=sync -conf=/tmp/RedisShake/conf/redis-shake.conf

