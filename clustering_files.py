import os
import subprocess
from shutil import move
from shutil import copy
from itertools import groupby
import zipfile

# Where the files are originally stored
# src_path = "C:\\temp\\src\\"
#src_path = "/home/lut/3gpp_lab/All_Tdocs/"

src_path = "/home/lut/3gpp_lab/3gpp_simulation/"

# Where the group folders will go
dest_path = "/home/lut/3gpp_lab/3gpp_simulation/organized/"

file_path = "/home/lut/PycharmProjects/PythonProject/"

# Open up the file containing the list of files
with open(file_path + "list_of_files.txt") as txt:
    lines = txt.readlines()  # Read the file

    i = (list(g) for _, g in groupby(lines, key='\n'.__ne__))
    list_of_groups = [a + b for a, b in zip(i, i)]

    # Iterate through each group
    for group in list_of_groups:
        folder_name = dest_path + group[0].replace("\n", "") + "/"
        # folder_name = dest_path

        if not os.path.exists(folder_name):
            # Create a folder for each group if it doesn't already exist
            os.mkdir(folder_name)

        # Move over each file in the group. The last element in the group is a newline character
        counter = 0
        for file in group:
            if counter > 0:
                if file != "\n":
                    #print(file[:10])
                    #print(file.replace("\t", "_"))
                    file1 = file.replace("\t", "_")
                    file2 = file1.replace(" ","_")
                    file3 = file2.replace(".","")
                    file4 = file3.replace("&", "and")
                    file5 = file4.replace("(","")
                    file6 = file5.replace(")","")
                    print(file6.replace("\n",""))

                    # Opening zip files, considering that all 3GPP files are following
                    # the patter of 10 characters before extension (.zip) to define the Tdoc Number
                    # example: R1-2507292.zip
                    z = zipfile.ZipFile(src_path + file[:10] + '.zip')

                    # Open the full ZIP stack
                    for f in z.infolist():
                        print('file size = ',str(f.file_size))

                        if f.file_size > 8000:
                            data = z.read(f)

                            #mapping the correct extension
                            extension_file_0 = f.filename
                            extension_file_1 = extension_file_0[-3:]
                            print(extension_file_1)
                            if extension_file_1 == 'ocx':
                                new_name = folder_name + file6.replace("\n","") + '.docx'
                            else:
                                new_name = folder_name + file6.replace("\n", "") + '.doc'
                            with open(new_name, 'wb') as fh:
                                    fh.write(data)

                        print("\n")

            counter = counter + 1

