from lib.classes_3gpp import getting3gppInfoFiles

####### Other possibilities to call the library:  ##############
#import lib
#import lib.reading_3gpp_excel
#from lib import read_excel_tdoc_number
#from lib.classes_3gpp import ReadingZipFilesToDoc
#from .reading_3gpp_excel import read_excel_tdoc_number

#creating an instance of the class getting3gppInfoFiles (the path and file xlsx is introduced dynamically)
instance1 = getting3gppInfoFiles()

# Examples:
#
# Case 1: to process all Agenda Items use the method "process_all"
# Example: instance1.process_all()
#instance1.process_all()

# Case 2: to process specific Agenda Item use the method "process_individual_ai"
# Examples: instance1.process_individual_ai()
instance1.process_individual_ai()


