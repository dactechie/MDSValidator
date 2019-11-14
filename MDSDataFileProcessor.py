import os
import sys
from time import time
from datetime import datetime
import click

from logger import logger
from AOD_MDS.helpers import log_results, read_data, read_header
from rule_checker.JSONValidator import JSONValidator
from rule_checker.MJValidationError import MJValidationError
from utils.ExcelWriter import write_data_to_book
from utils.files import get_latest_data_file, get_result_filename
from utils.dates import get_period_dict
from rule_checker.constants import MODE_LOOSE
#import pprint

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

def get_json_validator(start_end, schema_dir_name, schema_file_name, program=''):
    schema_dir = os.path.join(os.getcwd(), schema_dir_name)
    schema_file = os.path.realpath(os.path.join(schema_dir, schema_file_name))
    return JSONValidator(schema_dir, schema_file, start_end, program=program) 


def get_valid_header_or_die(filename, validator, mode):

    header = read_header(filename)
    missing_headers, fixed_header, header_warnings = validator.validate_header(header, mode=mode)
    if missing_headers:
        logger.critical(f"Missing Headers  {missing_headers} \n warnings {header_warnings}")
        sys.exit(0)

    return fixed_header, header_warnings


def get_data_or_die(filename, mds_header, hmap, start_end, all_eps=None):

    data = read_data(filename, mds_header, hmap, start_end, all_eps=all_eps)
    if not data or not data['episodes'] or len(data['episodes']) < 1 :
        logger.critical("No data. Quitting...")
        sys.exit(0)
    
    return data



@click.command()
@click.option('--data_file', '-d',
              help='Default: use the latest .csv file in the input folder.')
@click.option('--all_eps/--closed_only', '-a/-c', default=True,
              help='Validate only closed episodes. Default is to validate all episodes',
              show_default=True)
@click.option('--errors_only', '-e', help='Output only the rows with errors.', default=False,
                show_default=True, type=click.BOOL)
@click.option('--start_date', '-t', type=click.DateTime(formats=["%Y-%m-%d"]),
              help='The number of the starting month of the reporting period . Eg.: 2019-07-01',
              required=False)
@click.option('--program', '-p', type=click.Choice(['TSS', 'Arcadia-Resi', 'Other']),
              help='Some logic rules are specific to a team.' + \
                    'Default setting is to just apply just MDS rules.',
              default='TSS', show_default=True)
@click.option('--reporting_period', '-r', type=click.Choice(["12", "6", "3", "1"]),
              help='reporting period window.',
              default="3", show_default=True)
@click.option('--nostrict/--strict', '-s/-S', default=False,
              help='Accept/Reject imperfect data files with known aliases.' +
                   '\n1: reject (flag as errors)', show_default=True)
def main(data_file, all_eps, errors_only, start_date, program='', reporting_period="3", nostrict=False):
  if not start_date:
    start_date = datetime(2019,7,1)
    # logger.error("Start Date is required. Quitting")
    # sys.exit()

  FILENAME = None
  if not data_file or data_file =='None':
      FILENAME = get_latest_data_file()
  else:
      FILENAME =  os.path.join('input', data_file)
  
  if not FILENAME:
      logger.error("No input file. Quitting.")
      sys.exit()
  
  print(f"\t ***** Going to process {FILENAME} \n")

  exe(FILENAME, all_eps, errors_only, start_date, program=program, period=reporting_period, nostrict=nostrict)
  
  logger.info("\t ...End of Program...\n")



def exe(data_file, all_eps, errors_only, start_date, program='', period="3", nostrict=False):
  
  start_time = time()
 
  st_ed = get_period_dict(start_date, period_months=int(period))

  jv = get_json_validator(st_ed, schema_dir_name='AOD_MDS/schema/',
                          schema_file_name='schema.json',                          
                          program=program)
  
  mds_header, header_warnings = get_valid_header_or_die(data_file, validator=jv, mode=nostrict)
  
  
  data = get_data_or_die(data_file, mds_header, header_warnings, st_ed, all_eps=all_eps)
  
  verrors, warnings =  jv.validate(data, mode=nostrict)
  
  end_time = time()

  if warnings == -1:
    logger.error('Exiting....')
    sys.exit()

  # if any(v['field'] for k, v in verrors.items() if 'field' in v[0] and v[0]['field'] == '<>'):
  #   sys.exit(-1)

  
  #log_results(verrors, warnings, header_warnings)
  logger.info(f"\n\t ...End of validation... \n\t Processing time {round(end_time - start_time,2)} seconds. ")


  
  #pprint.pprint (verrors)
  logger.info("\t ...Writing results to spreadsheet..\n")    
  result_book = write_data_to_book(data['episodes'], verrors,
                                    get_result_filename(data_file, all_eps, st_ed, program), errors_only)
  
  return result_book


if __name__ == '__main__':   
    #main()
    sys.exit(main(sys.argv[1:]))
