import os
import sys
#from tes1t_data import setup_test_data
from time import time
import logging
import click

from ExcelWriter import write_data_to_book
from helpers import log_results, read_data, read_header
from JSONValidator import JSONValidator
from MJValidationError import MJValidationError
from utils import get_latest_data_file, get_result_filename
from constants import MODE_LOOSE

logger = None

def setup_logger(filename=__name__):
    global logger
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler = logging.FileHandler('mj.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


# logger = logging.getLogger("__main__")

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


def get_valid_header_or_die(filename, validator, mode=MODE_LOOSE):

    header = read_header(filename)
    missing_headers, fixed_header, header_warnings = validator.validate_header(header, mode=mode)
    if missing_headers:
        logger.critical(f"Missing Headers  {missing_headers} \n warnings {header_warnings}")
        sys.exit(0)

    return fixed_header, header_warnings
    #return header,  header_warnings


def get_data_or_die(filename, mds_header, hmap, all_eps=None):

    data = read_data(filename, mds_header, hmap, all_eps=all_eps)
    if not data or not data['episodes'] or len(data['episodes']) < 1 :
        logger.critical("No data. Quitting...")
        sys.exit(0)
    
    return data


@click.command()
@click.option('--data_file', '-d',
              help='Default: use the latest .csv file in the input folder.',
              show_default=True)
@click.option('--all_eps/--closed_only', '-a/-c', default=True,
              help='Validate only closed episodes. Default is to validate all episodes',
              show_default=True)
@click.option('--nostrict/--strict', '-s/-S', default=MODE_LOOSE,
              help='Accept/Reject imperfect data files with known aliases.' +
                   '\n1: reject (flag as errors)', show_default=True)
@click.option('--errors_only', '-e', help='Output only the rows with errors.',
                show_default=True)
def main(data_file, all_eps, nostrict, errors_only):
    # data = setup_test_data('./data copy.csv')
    # os.chdir("../..")   # when called from xwin (from excel), the python path is in the .\venv(mds)\Scripts folder,
    #                     # this breaks the paths for loading the schema etc. which are here .\schema
               # 'input\Final-Day.csv' #r'input\Arcadia_Resi.csv' #
    
    FILENAME = None
    if not data_file:
        FILENAME = get_latest_data_file('input')
    else:
        FILENAME =  os.path.join('input', data_file) #r'input\Final-Day.csv' # r'input\2019.08.23 TSS AMDS Full unchecked.csv' #  r'input\Arcadia-Day-Jan-Jun.csv'
    
    setup_logger(FILENAME)
    global logger
    # logger.info(f"Strict Mode: {nostrict}")

    start_time = time()

    jv = get_json_validator(schema_dir_name='schema/',
                            schema_file_name='schema.json')
    
    mds_header, header_warnings = get_valid_header_or_die(FILENAME, validator=jv, mode=nostrict)
    data = get_data_or_die(FILENAME, mds_header,  header_warnings, all_eps=all_eps)
    
    verrors, warnings =  jv.validate(data, mode=nostrict)
    
    end_time = time()
    #log_results(verrors, warnings, header_warnings)
    logger.info(f"\n\t ...End of validation... \n\t Processing time {round(end_time - start_time,2)} seconds. ")
    
    logger.info("\t ...Writing results to spreadsheet..\n")    
    result_book = write_data_to_book(data['episodes'], verrors,
                                     get_result_filename(FILENAME, all_eps), errors_only)
    logger.info("\t ...End of Program...\n")
    return result_book


if __name__ == '__main__':
    main()
    #sys.exit(main(sys.argv))
    # #data = setup_test_data('./data copy.csv')
