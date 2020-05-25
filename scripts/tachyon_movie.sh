#! /bin/bash
shopt -s expand_aliases
alias tachyon='/Applications/VMD\ 1.9.3.app/Contents/vmd/tachyon_MACOSXX86'

name=$1
dir=$2
dat_files=($2/$1*.dat)

for file in "${dat_files[@]}"; do
    tachyon $file -o "${file%.*}.tga"
done
printf "Cleaning movie directory...\n"
rm $2/$1*.dat

printf "Assembling '${1}' movie...\n"
convert -delay 1 -quality 100 $2/*.tga $2/$1.mpg

printf "Cleaning movie directory...\n"
rm $2/$1*.tga
printf "Done.\n"
