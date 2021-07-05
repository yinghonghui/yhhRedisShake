wget https://golang.google.cn/dl/go1.16.5.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.16.5.linux-amd64.tar.gz
vim ~/.bashrc
export PATH=$PATH:/usr/local/go/bin
source ~/.bashrc
set GOARCH=amd64
set GOOS=linux
export GOPROXY=https://goproxy.cn
go build /root/yhhRedisShake/src/redis-shake/main
mv /root/yhhRedisShake/src/main /root/yhhRedisShake/conf/
./main -type=sync -conf=/tmp/RedisShake/conf/redis-shake.conf