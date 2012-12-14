#!/bin/bash

##    IMPORTANT    ##
##  YOU MUST PLACE THIS SCRIPT IN YOUR SABNZBD SCRIPTS FOLDER ##
##  AND YOU MUST SET THE COMICTAGGER DIRECTORY/PATH BELOW ##
##  FINALLY, YOU MUST MAKE THIS FILE EXECUTABLE (sudo chmod a+x /path/to/cmtagmylar.sh) ##


## Set the directory in which comictagger.py is located - IMPORTANT - ##
comictaggerpath=/path/to/comictagger/




## Sets up other directories ##
downloadpath="$1"/
sabnzbdscriptpath=$(dirname $0)
mkdir "$downloadpath"temp/
comicpath="$downloadpath"temp/
cd "$comicpath"

## Takes all .cbr and .cbz files and dumps them to processing directory ##
for file in "$downloadpath"*.cbr "$downloadpath"*.cbz; do
mv "$file" "$comicpath"
done

## Changes filetype extensions when needed ##
for file in "$comicpath"*cbr; do
filetype=$(file "$file")
if [[ "$filetype" == *Zip* ]]
then mv "$file" "${file%.cbr}.cbz"
else echo "cbr is good to go"
fi
done
for file in "$comicpath"*cbz; do
filetype=$(file "$file")
if [[ "$filetype" == *RAR* ]]
then mv "$file" "${file%.cbz}.cbr"
else echo "cbz is good to go"
fi
done

## Changes any cbr files to cbz files for insertion of metadata ##
for file in "$comicpath"*.cbr; do
mv "$file" "${file%.cbr}.rar"
done
for file in "$comicpath"*.rar; do
convertrarname="$file"
unrar x "$file"
rm "$file"
done
for D in ./* ; do
zip -rm "$convertrarname.zip" "$D" -x "*.cbz" "*.pl"
done
for file in "$comicpath"*.zip; do
mv "$file" "${file%.rar.zip}.cbz"
done

## Clean up temp directory and move files back to original directory ##
for file in "$comicpath"*.cbz; do
python "$comictaggerpath"comictagger.py -s -t cr -f -o  "$file"
##  Uncomment the below line and comment out the above line for Mac OSX users  ##
##  /Applications/ComicTagger.app/Contents/MacOS/ComicTagger -s -t cr -f -o  "$file"
mv "$file" "$downloadpath"
done
cd "$sabnzbdscriptpath"
rm -r "$comicpath"


## Will Run Mylar Post=processing In Future ##
