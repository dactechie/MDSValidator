import os
import xlwings as xw
from MDSDataFileProcessor import main2
from logger import logger

def fetch_validation_results(source_file):

    result_file_name = main2(source_file)

    wb = xw.books.active
    currentBookSheet = wb.sheets['Data']
        
    result_file = os.path.realpath(os.path.join(os.getcwd(), result_file_name))

    logger.info(f"result file name  {result_file}")

    sourceBook = xw.Book(result_file)
    sht = sourceBook.sheets['loaded']

    sht.api.Copy(Before=currentBookSheet.api)
    sourceBook.close()

    logger.info(f"Finished writing to result file. It was closed.")
