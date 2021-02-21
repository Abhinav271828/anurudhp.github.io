#!/bin/bash

if [ "$#" -lt 2 ] || [ ! -f "$1" ] ; then
  echo "Usage: $0 <path/to/input/file.lhs> <path/to/output/file.md>"
  exit 1
fi

input=$1
output=$2

# log
echo -n "Compiling $input to $output... "

# create empty file
echo -n "" > $output

# append YAML metadata (which is dropped by pandoc)
runhaskell $(dirname "$0")/getYAMLMetadata.hs $input >> $output
echo "" >> $output

# convert
pandoc --from markdown+lhs --to markdown $input >> $output

# fix code tags
sed -i "s/sourceCode literate haskell/haskell/g" $output
sed -i 's#{.sourceCode .literate .haskell}#haskell#g' $output
sed -i 's#{.haskell}#haskell#g' $output
sed -i 's/^\\#\\#\\#/###/g' $output

