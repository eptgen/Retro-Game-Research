#!/bin/bash

replacements=(0 45 45 45 45 45 45 45 45 45 45 45 45 13 14 15 16 0 0 0 0 0 0 0 0 0 0 0 0 29 30 31 32 16 16 16 16 16 16 16 16 16 16 16 16 45 46 47 48 61 61 61 61 61 61 61 61 61 61 61 61 61 62 63)

filename=$1
namelen=${#filename}
# echo $namelen
bgrep -E "\x3F[\x00-\x20][\x01-\x20]" $filename > search.txt

locbegin=$(($namelen + 2))
locend=$(($namelen + 9))

j=1

while read line; do

  lochex=$(echo $line | cut -c$locbegin-$locend)
  loc=$((16#$lochex))
  startpalette=$((16#$(xxd -p -l1 -s $(($loc + 9)) $filename)))
  endpalette=$((16#$(xxd -p -l1 -s $(($loc + 10)) $filename)))
  palettelen=$(($endpalette - $startpalette))

  if [ $palettelen -lt 1 ]
  then
    continue
  fi

  shouldcontinue=0
  for i in $(seq $palettelen)
  do
    byte=$((16#$(xxd -p -l1 -s $(($loc + 10 + $i)) $filename)))
    if [ $byte -gt 63 ]
    then
      shouldcontinue=1
    fi
  done

  if [ $shouldcontinue = 1 ]
  then
    continue
  fi

  echo "Palette #$j:"
  echo "Changing colors $startpalette to $endpalette"
  echo "Colors:"
  for i in $(seq $palettelen)
  do
    byte=$(xxd -p -l1 -s $(($loc + 10 + $i)) $filename)
    echo -n "$byte "
  done
  echo ""
  printf "Location: %08x\n" $(($loc + 8))
  echo ""

  j=$(($j + 1))

done < search.txt






















rm search.txt
