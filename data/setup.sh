#!/bin/sh
apt-get install p7zip-full

for file in *.7z
do
  7z e "$file"
done
