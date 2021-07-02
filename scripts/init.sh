wget https://golang.google.cn/dl/go1.16.5.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.16.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
set GOARCH=amd64
set GOOS=linux
export GOPROXY=https://goproxy.cn
go build ./main.go
./main -type=sync -conf=/tmp/RedisShake/conf/redis-shake.conf