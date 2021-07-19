#!/bin/bash

touch search.txt

numbefore=30
numafter=60

filename=$1
location=$((16#$2))

count=$(($numbefore + $numafter))
begin=$(($location - $numbefore))

dd if=$filename skip=$begin bs=1 count=$count of=search.txt &> /dev/null
cat search.txt

rm search.txt
