Sabnzbd-Comictagger-Mylar-Script
================================

A python script to post-process comics


The cmtaggermylar.py script must be placed in your sabnzbd scripts directory in order to process and tag comics once downloaded by sabnzbd.

The provided ComicRN.py script should replace the one included with the Mylar install, should you also be using Mylar.

You may have to manually set the directory for your comictagger installation by editing the cmtagger.py file on the line appropriate for your OS (though some best guesses are used by default).

This does the following:

1.  Checks to make sure the downloaded comic has the correct extension, and changes it if not

2.  Converts cbr files to cbz for tagging

3.  Inserts comicvine metadata compliant with both ComicRack and ComicZeal

4.  Calls the normal mylar post-processing


Comictagger can be found here:  http://code.google.com/p/comictagger/
Mylar can be found here:   https://github.com/evilhero/mylar