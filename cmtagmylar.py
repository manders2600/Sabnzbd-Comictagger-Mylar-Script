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

## Set the directory in which comictagger and other external commands are located - IMPORTANT - ##
# ( User may have to modify, depending on their setup, but these are some guesses for now )

if platform.system() == "Windows":
  comictagger_cmd = "C:\Program Files\ComicTagger\comictagger.exe"
  # http://www.win-rar.com/download.html
  unrar_cmd =       "C:\ProgramFiles\WinRAR\unrar.exe"
  # http://stahlforce.com/dev/zip.exe
  zip_cmd =         "zip.exe"
  
elif platform.system() == "Darwin":  #Mac OS X
  comictagger_cmd = "/Applications/ComicTagger.app/Contents/MacOS/ComicTagger"
  unrar_cmd =       "/usr/local/bin/unrar"
  zip_cmd =         "/usr/bin/zip"
  
else:
  comictagger_cmd = "/path/to/comictagger/comictagger.py"
  unrar_cmd =       "/usr/bin/unrar"
  zip_cmd =         "/usr/bin/zip"

if not os.path.exists( comictagger_cmd ):
  print "ERROR:  can't find the ComicTagger program: {0}".format( comictagger_cmd )
  print "        You probably need to edit this script!"
  sys.exit( 1 )

file_conversion = True
if not os.path.exists( unrar_cmd ) or not os.path.exists( zip_cmd ):
  print "WARNING:  can't find the zip or unrar command, or both."
  print "          File conversion not available"
  print "          You probably need to edit this script, or install the missing tools, or both!"
  file_conversion = False

file_extension_fixing = True
if not os.path.exists( unrar_cmd ):
  print "WARNING:  can't find the unrar command" 
  print "          Some file extension fixing not available"
  print "          You probably need to edit this script, or install the unrar tool, or both!"
  file_extension_fixing = False


## Sets up other directories ##
scriptname = os.path.basename( sys.argv[0] )
downloadpath = os.path.abspath(sys.argv[1]) 
sabnzbdscriptpath = os.path.dirname( sys.argv[0] )
comicpath = os.path.join( downloadpath , "temp" )
unrar_folder = os.path.join( comicpath , "unrard" )

print "----------------------------------------------"
print "Running {0}, the Post-SabNZBd/Mylar script".format( scriptname )
print "----------------------------------------------"

if os.path.exists( comicpath ):
  shutil.rmtree( comicpath )
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
	print "{0}: renaming {1} to be a cbz".format( scriptname, os.path.basename( f ) )

if file_extension_fixing:
  cbz_list = glob.glob( os.path.join( comicpath, "*.cbz" ) )
  for f in cbz_list:
	try:
	  rar_test_cmd_output = "is not RAR archive" #default, in case of error
	  rar_test_cmd_output = subprocess.check_output( [ unrar_cmd, "t", f ] )
	except:
	  pass
	if not "is not RAR archive" in rar_test_cmd_output:
	  base = os.path.splitext( f )[0]
	  shutil.move( f, base + ".cbr" )
	  print "{0}: renaming {1} to be a cbr".format( scriptname, os.path.basename( f ) )

# Now rename all CBR files to RAR
cbr_list = glob.glob( os.path.join( comicpath, "*.cbr" ) )
for f in cbr_list:
  base = os.path.splitext( f )[0]
  shutil.move( f, base + ".rar" )

## Changes any cbr files to cbz files for insertion of metadata ##
if file_conversion:
  rar_list = glob.glob( os.path.join( comicpath, "*.rar" ) )
  for f in rar_list:
	print "{0}: converting {1} to be zip format".format( scriptname, os.path.basename( f ) )
	basename = os.path.splitext( f )[0]
	zipname = basename + ".cbz"

	# Move into the folder where we will be unrar-ing things
	os.makedirs( unrar_folder )
	os.chdir( unrar_folder )

	subprocess.Popen( [ unrar_cmd, "x", f ] ).communicate()  # Probably not portable to Windows (need path of unrar.exe)
	#os.unlink( f )
	subprocess.Popen( [ zip_cmd, "-rm", zipname, "." ] ).communicate()  # Not portable to Windows (no command-line zip!!)

	# get out of unrar folder and clean up
	os.chdir( comicpath )
	shutil.rmtree( unrar_folder )

## Tag each CBZ, and move it back to original directory ##
cbz_list = glob.glob( os.path.join( comicpath, "*.cbz" ) )
for f in cbz_list:
	subprocess.Popen( [ comictagger_cmd, "-s", "-t", "cr", "-f", "-o", "--verbose", "--nooverwrite", f ] ).communicate()
	subprocess.Popen( [ comictagger_cmd, "-s", "-t", "cbl", "-f", "-o", "--verbose", "--nooverwrite", f ] ).communicate()
	shutil.move( f, downloadpath )

## Clean up temp directory  ##
os.chdir( sabnzbdscriptpath )
shutil.rmtree( comicpath )

## Will Run Mylar Post=processing In Future ##
