#!/bin/bash
#
# https://mrjbq7.github.io/ta-lib/install.html
#

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xcfv ta-lib-0.4.0-src.tar.gz
cd ta-lib-0.4.0-src/ta-lib
./configure --prefix=/usr
make
sudo make install