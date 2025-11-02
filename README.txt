STEP_0: Downloading all Tdocs using FTP as anonymous



STEP_1: grouping Zip Files:
==================
"moving_files.py" 
which is using the list of file names in "list_of_files.txt"
Note: include the name of desired folder at the beginning of each list group




STEP_2: Processing files: 
(1 )unzip, 
(2) normalizing file names (deleting_spaces.py), 
(3) Convertig all to PDF (script.sh), 
(4) joining all PDFs into a unique file
=========================


UNZIP MANY ZIP FILES SIMULTANEOUSLY
-----------------------------------

unzip \*.zip




Joining many PDF files
-------------------

gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=finished.pdf R1*.pdf




MASTER SCRIPT:
=============
All the process was compilated in the following script file
master.sh

Run 

./master.sh <NAME_of_FILE>  in shell screen. 



