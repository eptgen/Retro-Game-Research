#!/bin/bash

numbefore=30
numafter=60

filename=$1
location=$((16#$2))

count=$(($numbefore + $numafter))
begin=$(($location - $numbefore))

xxd -l$count -s $begin $filename
