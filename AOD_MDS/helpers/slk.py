
from utils import (get_23, get_235, cleanse_string)


def getSLK(firstname, lastname, DOB_str, sex_str):
    """
    Expects DOB_str to be in "ddmmyyyy" or "dd/mm/yyyy" format
    sex_str must be 'Male' or 'Female' , everything else is converted to 9
    """
    if not lastname or not firstname:
      return ""
    last = get_235(cleanse_string(lastname))
    first = get_23(cleanse_string(firstname))
    
    name_part = (last + first).upper()
    
    if sex_str == 'Male':
        sex_str = '1'
    elif sex_str == 'Female':
        sex_str = '2'
    else:
        sex_str = '9'   # TODO    'if not unknown, add a Warning ?'
    
    return name_part + DOB_str.replace("/","") + sex_str # .replace("/","")
