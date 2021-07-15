
touch search.txt

for rom in unzipped/*
do
  bgrep -E "\x3F[\x00-\x20][\x01-\x20]" "$rom" > search.txt

  namelen=${#rom}
  locbegin=$(($namelen + 2))
  locend=$(($namelen + 9))

  j=0

  while read line; do

    lochex=$(echo $line | cut -c$locbegin-$locend)
    loc=$((16#$lochex))
    startpalette=$((16#$(xxd -p -l1 -s $(($loc + 9)) "$rom")))
    endpalette=$((16#$(xxd -p -l1 -s $(($loc + 10)) "$rom")))
    palettelen=$(($endpalette - $startpalette))

    if [ $palettelen -lt 1 ]
    then
      continue
    fi

    shouldcontinue=0
    for i in $(seq $palettelen)
    do
      byte=$((16#$(xxd -p -l1 -s $(($loc + 10 + $i)) "$rom")))
      if [ $byte -gt 63 ]
      then
        shouldcontinue=1
      fi
    done

    if [ $shouldcontinue = 1 ]
    then
      continue
    fi

    j=$(($j + 1))
  done < search.txt

  echo $rom: found $j palettes
done










































rm search.txt
