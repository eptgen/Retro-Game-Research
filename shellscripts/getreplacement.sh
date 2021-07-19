#!/bin/bash

replacements=(0 45 45 45 45 45 45 45 45 45 45 45 45 13 14 15  16 0 0 0 0 0 0 0 0 0 0 0 0 29 30 31  32 16 16 16 16 16 16 16 16 16 16 16 16 45 46 47  48 61 61 61 61 61 61 61 61 61 61 61 61 61 62 63)

while true
do
  read answer
  answer=$((16#$answer))
  changeTo=${replacements[$answer]}
  printf "%02x\n" $changeTo
done
