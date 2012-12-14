#!/usr/bin/python

##    IMPORTANT    ##
##  YOU MUST PLACE THIS SCRIPT IN YOUR SABNZBD SCRIPTS FOLDER ##
##  AND YOU MUST SET THE COMICTAGGER DIRECTORY/PATH BELOW ##
##  FINALLY, YOU MUST MAKE THIS FILE EXECUTABLE (sudo chmod a+x /path/to/cmtagmylar.py) ##

import os
import sys
import glob
import platform
import shutil
import zipfile
import subprocess
import commands

## Set the directory in which comictagger executable is located - IMPORTANT - ##
# ( User may have to modify, depending on their setup, but these are some guesses for now )
if platform.system() == "Windows":
  comictaggercommand = "C:\Program Files\ComicTagger\comictagger.exe"
elif platform.system() == "Darwin":
	comictaggercommand = "/Applications/ComicTagger.app/Contents/MacOS/ComicTagger"
else:
	comictaggercommand = "/home/marktest/Downloads/comictagger-src-0.9.1-beta/comictagger.py"

## Sets up other directories ##
downloadpath = "/share/comics/process/THYR" 
sabnzbdscriptpath = os.path.dirname( sys.argv[0] )
comicpath = os.path.join( downloadpath , "temp" )
unrar_folder = os.path.join( comicpath , "unrard" )

os.makedirs( comicpath )

# make a list of all CBR and CBZ files in downloadpath
filename_list = glob.glob( os.path.join( downloadpath, "*.cbz" ) )
filename_list.extend( glob.glob( os.path.join( downloadpath, "*.cbr" ) ) )

## Takes all .cbr and .cbz files and dumps them to processing directory ##
for f in filename_list:
	shutil.move( f, comicpath)

## Changes filetype extensions when needed ##
cbr_list = glob.glob( os.path.join( comicpath, "*.cbr" ) )
for f in cbr_list:
	if zipfile.is_zipfile( f ):		
		base = os.path.splitext( f )[0]
		shutil.move( f, base + ".cbz" )

cbz_list = glob.glob( os.path.join( comicpath, "*.cbz" ) )
for f in cbz_list:
	file_cmd_output = commands.getoutput("file test.zip")  # Not portable to Windows
	if "RAR" in file_cmd_output:
		base = os.path.splitext( f )[0]
		shutil.move( f, base + ".cbr" )

# Now rename all CBR files to RAR
cbr_list = glob.glob( os.path.join( comicpath, "*.cbr" ) )
for f in cbr_list:
	base = os.path.splitext( f )[0]
	shutil.move( f, base + ".rar" )

## Changes any cbr files to cbz files for insertion of metadata ##
rar_list = glob.glob( os.path.join( comicpath, "*.rar" ) )
for f in rar_list:
	basename = os.path.splitext( f )[0]
	zipname = basename + ".zip"

	# Move into the folder where we will be unrar-ing things
	os.makedirs( unrar_folder )
	os.chdir( unrar_folder )
	
	subprocess.Popen( [ "unrar", "x", f ] )  # Probably not portable to Windows (need path of unrar.exe)
	os.unlink( f )
	subprocess.Popen( [ "zip", "-rm", zipname, "*" ] )  # Not portable to Windows (no command-line zip!!)
	
	# get out of unrar folder and clean up
	os.chdir( comicpath )
	shutil.rmtree( unrar_folder )
	
## Tag each CBZ, and move it back to original directory ##
cbz_list = glob.glob( os.path.join( comicpath, "*.cbz" ) )
for f in cbz_list:
	subprocess.Popen( [ comictaggercommand, "-s", "-t", "cr", "-f", "-o",  f ] )
	shutil.move( f, downloadpath )
	
## Clean up temp directory  ##
os.chdir( sabnzbdscriptpath )
shutil.rmtree( comicpath )


## Will Run Mylar Post=processing In Future ##
