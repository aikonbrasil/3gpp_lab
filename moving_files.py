import os
from shutil import move
from itertools import groupby

#Where the files are originally stored
#src_path = "C:\\temp\\src\\"
src_path = "/home/lut/3gpp_lab/All_Tdocs/"

#Where the group folders will go
dest_path = "/home/lut/3gpp_lab/All_Tdocs/destination/"

#Open up the file containing the list of files
with open(src_path + "list_of_files.txt") as txt:
    lines = txt.readlines() #Read the file

    i = (list(g) for _, g in groupby(lines, key='\n'.__ne__))
    list_of_groups = [a + b for a, b in zip(i, i)]

    #Iterate through each group
    for group in list_of_groups:
        folder_name = dest_path + group[0].replace("\n","") + "/"
        #folder_name = dest_path
        
        if not os.path.exists(folder_name):
            #Create a folder for each group if it doesn't already exist
            os.mkdir(folder_name)
        
        #Move over each file in the group. The last element in the group is a newline character
        counter = 0
        for file in group:
            if counter >0:
                if file != "\n":
                    move(src_path + file.replace("\n","")+'.zip',folder_name + file.replace("\n","")+'.zip')
                    print(src_path + file.replace("\n","")+'.zip')
            counter = counter + 1

