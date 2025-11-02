import pandas as pd
import zipfile
import os
import openpyxl
import numpy as np

class getting3gppInfoFiles:

    def __init__(self):

        self.file_location = input('Enter the path of xlsx file: ')
        #self.desired_ai = input('Enter the desired Agenda Item: ')
        self.df = pd.read_excel(self.file_location)

        self.ws = openpyxl.load_workbook(self.file_location)['TDoc_List']
        folder_raw_source = os.path.dirname(self.file_location)
        # SCRIPT that NORMALIZE NAMES, when names includes spaces in between
        # TODO: generalize this code
        for f in os.listdir(folder_raw_source + '/'):
            r = f.replace(" ", "")
            # if( r != f):
            #    os.rename(f,r)
            x = r.replace("(", "")
            # if (x != f):
            #    os.rename(f,x)
            y = x.replace(")", "")
            if (x != f):
                os.rename(folder_raw_source + '/'+f, folder_raw_source + '/'+y)

        cells_without_hyperlink = []
        cells_with_hyperlink = []
        for ii in range(1513):
            try:
                self.ws.cell(row=ii + 1, column=1).hyperlink.target
                cells_with_hyperlink = cells_with_hyperlink + [ii - 1]

            except AttributeError:
                cells_without_hyperlink = cells_without_hyperlink + [ii - 1]

        #Where the raw files are located
        #self.src_path = "/home/lut/3gpp_lab/3gpp_simulation/"
        self.src_path = folder_raw_source + '/'

        # Where the group folders will go
        #self.dest_path = "/home/lut/3gpp_lab/3gpp_simulation/organized/"
        self.dest_path = folder_raw_source + '/organized/'

        if not os.path.exists(self.dest_path):
            # Create a folder for each group if it doesn't already exist
            os.mkdir(self.dest_path)

        #### --> manual script to delete files that were withdrawn (no available files)
        # Status do Tdoc (it is obsolete now, because the Hyperlink existence is more specific for the Tdoc Number column)
        tdoc_status = self.df['TDoc Status']
        tdoc_withdraw_index = tdoc_status['withdrawn' != tdoc_status].index

        s1 = pd.DataFrame([])
        for index, row in self.df.iterrows():
            #if index in tdoc_withdraw_index:
            if index in cells_with_hyperlink:
                s1 = pd.concat([s1, row], axis=1)
        #s2 = s1.transpose()
        self.df = s1.transpose()



    def get_all_agenda_items(self):
        vector_agenda_item = self.df['Agenda item']
        condition = vector_agenda_item.duplicated(keep='first')
        only_unique_ais = vector_agenda_item[~condition]

        return only_unique_ais.to_list()

    def read_excel_tdoc_number(self,desired_ai):

        #tdoc_withdraw_indexvalues = tdoc_withdraw_index.values


        #Selecting the desired columns to process
        tdoc_number = self.df['TDoc']

        #Company_name_source = self.df['Source']
        agend_item = self.df['Agenda item']

        #ai_index = agend_item[agend_item == self.desired_ai].index
        ai_index = agend_item[agend_item == desired_ai].index

        tdoc_numbers_series = tdoc_number[ai_index]
        tdoc_numbers_list = tdoc_numbers_series.to_list()

        return tdoc_numbers_list

    def read_excel_source_name(self, desired_ai):
        # Selecting the desired columns to process
        company_name_source = self.df['Source']

        agend_item = self.df['Agenda item']

        #ai_index = agend_item[agend_item == self.desired_ai].index
        ai_index = agend_item[agend_item == desired_ai].index
        # AI_6g_values = agend_item[agend_item == self.desired_ai].values


        # series and list containing company names of specific Agenda Item
        names_companies = company_name_source[ai_index]
        names_companies_list = names_companies.to_list()

        return names_companies_list

    def process_individual_ai(self):

        # Generating the information before process files per AI
        desired_ai = input('Enter the desired Agenda Item: ')
        print('Processing Agenda Item # ' + str(desired_ai))
        names_companies_list = self.read_excel_source_name(desired_ai)
        tdoc_numbers_list = self.read_excel_tdoc_number(desired_ai)

        tdoc_numbers_sourceNames = []
        for a, b in zip(tdoc_numbers_list, names_companies_list):
            aux_tdoc_numbers_sourceNames = a + '\t' + b
            tdoc_numbers_sourceNames.append(aux_tdoc_numbers_sourceNames)

        #Scripts that aims to organize files on specific folders per AI
        folder_name = self.dest_path + desired_ai + "/"

        if not os.path.exists(folder_name):
            # Create a folder for each group if it doesn't already exist
            os.mkdir(folder_name)

        for spec_tdoc_number in tdoc_numbers_sourceNames:
            if spec_tdoc_number != "\n":
                # iteration for different impairments (no advisable characters in name files)
                file1 = spec_tdoc_number.replace("\t", "_")
                file2 = file1.replace(" ", "_")
                file3 = file2.replace(".", "")
                file4 = file3.replace("&", "and")
                file5 = file4.replace("(", "")
                file6 = file5.replace(")", "")
                #print(file6.replace("\n", ""))

                # Opening zip files, considering that all 3GPP files are following
                # the patter of 10 characters before extension (.zip) to define the Tdoc Number
                # example: R1-2507292.zip
                z = zipfile.ZipFile(self.src_path + spec_tdoc_number[:10] + '.zip')

                # Open the full ZIP stack
                for f in z.infolist():
                    #print('file size = ', str(f.file_size))
                    if f.file_size > 8000:
                        data = z.read(f)

                        # mapping the correct extension
                        extension_file_0 = f.filename
                        extension_file_1 = extension_file_0[-3:]
                        #print(extension_file_1)
                        if extension_file_1 == 'ocx':
                            new_name = folder_name + file6.replace("\n", "") + '.docx'
                        else:
                            new_name = folder_name + file6.replace("\n", "") + '.doc'
                        with open(new_name, 'wb') as fh:
                            fh.write(data)

        return 0

    def process_all(self):
        all_ais = self.get_all_agenda_items()
        for desired_ai in all_ais:
            print('Processing Agenda Item # ' + str(desired_ai))
            names_companies_list = self.read_excel_source_name(desired_ai)
            tdoc_numbers_list = self.read_excel_tdoc_number(desired_ai)

            tdoc_numbers_sourceNames = []
            for a, b in zip(tdoc_numbers_list, names_companies_list):
                aux_tdoc_numbers_sourceNames = a + '\t' + b
                tdoc_numbers_sourceNames.append(aux_tdoc_numbers_sourceNames)

            # outcome should be automatized with the name of the Agenda Item
            folder_name = self.dest_path + desired_ai + "/"

            if not os.path.exists(folder_name):
                # Create a folder for each group if it doesn't already exist
                os.mkdir(folder_name)

            for spec_tdoc_number in tdoc_numbers_sourceNames:
                if spec_tdoc_number != "\n":
                    # print(file[:10])
                    # print(file.replace("\t", "_"))
                    file1 = spec_tdoc_number.replace("\t", "_")
                    file2 = file1.replace(" ", "_")
                    file3 = file2.replace(".", "")
                    file4 = file3.replace("&", "and")
                    file5 = file4.replace("(", "")
                    file6 = file5.replace(")", "")
                    #print(file6.replace("\n", ""))

                    # Opening zip files, considering that all 3GPP files are following
                    # the patter of 10 characters before extension (.zip) to define the Tdoc Number
                    # example: R1-2507292.zip
                    z = zipfile.ZipFile(self.src_path + spec_tdoc_number[:10] + '.zip')

                    # Open the full ZIP stack
                    for f in z.infolist():
                        #print('file size = ', str(f.file_size))
                        if f.file_size > 8000:
                            data = z.read(f)

                            # mapping the correct extension
                            extension_file_0 = f.filename
                            extension_file_1 = extension_file_0[-3:]
                            #print(extension_file_1)
                            if extension_file_1 == 'ocx':
                                new_name = folder_name + file6.replace("\n", "") + '.docx'
                            else:
                                new_name = folder_name + file6.replace("\n", "") + '.doc'
                            with open(new_name, 'wb') as fh:
                                fh.write(data)
        return 0