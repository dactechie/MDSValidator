import os
import sys
from helpers import read_header, read_data, log_results
from JSONValidator import JSONValidator
from MJValidationError import MJValidationError
from ExcelWriter import write_data_to_book
#from tes1t_data import setup_test_data
from time import time

"""
    This module is to be made responsible for being the engine for orchestrating, the processing of incoming JSON data.
    1. Queue up a task for :
        a. pushing the data as-is into the database with timestamp etc.
        b. then reading it for cleansing and validation (including determining suggestions for SLK, and other values)
        c. writing the errors and warnings to the database
        d. returning the errors and warnings to the caller/client
    2. Queue up a 2nd task after 1.c, to write to excel file with color coded formatting
        then return the path to the new .xlsx to the user.
"""


def get_json_validator(schema_dir_name, schema_file_name):
    schema_dir = os.path.join(os.getcwd(), schema_dir_name)
    schema_file = os.path.realpath(os.path.join(schema_dir, schema_file_name))
    return JSONValidator(schema_dir, schema_file)


def get_valid_header_or_die(filename, validator, mode=0):

    header = read_header(filename)
    missing_headers, header_warnings = validator.validate_header(header,mode=mode)
    if missing_headers:
        print ("Missing Headers ", missing_headers, "\n warnings ", header_warnings)
        sys.exit(0)
        
    return header,  header_warnings


def get_data_or_die(filename, data_header, hmap):

    data = read_data(filename, data_header, hmap)
    if not data or not data['episodes'] or len(data['episodes']) < 1 :
        print("No data to validate. quitting...")
        sys.exit(0)
    
    return data


def main(args):
    #data = setup_test_data('./data copy.csv')
    FILENAME = 'AMDS Combined 12.08.19.csv' #  'Arcadia-Resi-Jan-Jun.csv' #'AMDS Combined 12.08.19.csv' #
    MODE = 0
    closed_eps_only= False
    start_time = time()

    jv = get_json_validator(schema_dir_name='schema/',
                            schema_file_name='schema.json')
    
    data_header, header_warnings = get_valid_header_or_die(FILENAME, validator=jv, mode=MODE)
    data = get_data_or_die(FILENAME, data_header,  header_warnings)
    
    #mode 0 : not strict - with warnings     #mode 1 : strict (no alias translations) - no warnings, all errors
    verrors, warnings =  jv.validate(data,mode=MODE, closed_eps_only=closed_eps_only)
    
    end_time = time()
    #log_results(verrors, warnings, header_warnings)
    print(f"\n \t\t ...End of validation... \n\t\t Processing time {round(end_time - start_time,2)} seconds. ")
    
    #print(f"\n\t\t Setup time {round(start_time - setup_time,2)}")
    print("\n\n \t\t ...Writing results to spreadsheet..\n")
    write_data_to_book(data['episodes'], verrors ,'./book1')
    print("\n \t\t ...End of Program...\n")

    

if __name__ == '__main__':
    sys.exit(main(sys.argv))
    # #data = setup_test_data('./data copy.csv')


