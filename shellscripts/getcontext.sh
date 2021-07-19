#!/bin/bash

touch search.txt

numbefore=30
numafter=60

filename=$1
location=$((16#$2))

num=0
for i in $(seq $(($location - $numbefore)) $(($location + $numafter)))
do
  byte=$(xxd -p -l1 -s $i $filename)
  printf "%s " $byte
  num=$(($num + 1))
  if [ $(($num % 16)) -eq 0 ]
  then
    printf "\n"
  fi
done

printf "\n"
