#!/bin/bash
unzip \*.zip
python deleting_spaces.py
./script.sh
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=all_$1.pdf R1*.pdf
