Sabnzbd-Comictagger-Mylar-Script
================================

A python script to post-process comics



Right now, this script only works when using the development version of mylar in my repository, though there is a pull request to have these changes merged into evilhero's repo.  Simply enter the path to cmtagmylar.py in the "Pre-scripts" box on the mylar config page, and you should be good to go.

You may have to manually set the directory for your comictagger installation by editing the cmtagger.py file on the line appropriate for your OS (though some best guesses are used by default).

This does the following:

1.  Checks to make sure the downloaded comic has the correct extension, and changes it if not

2.  Converts cbr files to cbz for tagging

3.  Inserts comicvine metadata compliant with both ComicRack and ComicZeal

4.  Calls the normal mylar post-processing


Comictagger can be found here:  http://code.google.com/p/comictagger/
Mylar can be found here:   https://github.com/evilhero/mylar
