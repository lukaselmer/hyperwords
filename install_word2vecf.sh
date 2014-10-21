#!/bin/sh
wget https://bitbucket.org/yoavgo/word2vecf/get/90e299816bcd.zip
unzip 90e299816bcd.zip
rm 90e299816bcd.zip
mv yoavgo-word2vecf-90e299816bcd/*.c .
mv yoavgo-word2vecf-90e299816bcd/*.h .
mv yoavgo-word2vecf-90e299816bcd/makefile .
rm -r yoavgo-word2vecf-90e299816bcd
make
