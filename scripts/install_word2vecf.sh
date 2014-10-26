#!/bin/sh
mkdir word2vecf
wget https://bitbucket.org/yoavgo/word2vecf/get/90e299816bcd.zip
unzip 90e299816bcd.zip
rm 90e299816bcd.zip
mv yoavgo-word2vecf-90e299816bcd/*.c word2vecf/.
mv yoavgo-word2vecf-90e299816bcd/*.h word2vecf/.
mv yoavgo-word2vecf-90e299816bcd/makefile word2vecf/.
rm -r yoavgo-word2vecf-90e299816bcd
make -C word2vecf