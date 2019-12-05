import os
from logger import logger

def get_latest_data_file(dir='input'):
    import glob
    
    list_of_files = glob.glob(os.path.join(dir,'*.csv')) # * means all if need specific format then *.csv
    if not any(list_of_files):
        logger.error("no input csv file in the input folder !")
        return None

    return max(list_of_files, key=os.path.getctime)


def get_result_filename(fullname, all_eps=True, program='TSS'):

    if not all_eps:
        output_fname_tags =f'{program}_closed_eps_period_'
    else:
        output_fname_tags = f'{program}_with_open_eps_period_'  
    logger.debug("outputfile tags :" + output_fname_tags)
    base = os.path.basename(fullname)
    input_filename = os.path.splitext(base)[0]
    return os.path.join("output", f"./{input_filename}_{output_fname_tags}")
