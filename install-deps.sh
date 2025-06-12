#! /usr/bin/env sh

cd /tmp

git clone https://github.com/Raisess/box
git clone https://github.com/Raisess/migrate

cd box && ./install.py && cd ..
cd migrate && ./install.py && cd ..
