import os
from collections import OrderedDict
from datetime import datetime
import re

alpha_pattern = re.compile(r'[\W_0-9]+')
cleanse_string = lambda string: alpha_pattern.sub('', string)

no_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
remove_unicode = lambda string: no_unicode_pattern.sub('', string)



def get_fields_value_string(data):
    data = OrderedDict(data)

    data_values_list = list(data.values())
    value_format = (' %s,' * len(data_values_list)).rstrip(',')

    fields = ','.join(data.keys())
    return fields, value_format, data_values_list


def get_formatted_sql(data, template, record_id):
    data = OrderedDict(data)

    keys_str = ','.join([f"`{k}`= %s" for k in data])
    sql_template = template.replace('__record_keys_format__', keys_str)

    replacement_list = list(data.values())
    replacement_list.append(record_id)

    return sql_template, replacement_list

    
def has_duplicate_values(*arr):
    """
    Checks if the first value in the passed-in list, appears in the rest of the list
    The 2nd item in the passed-in list is a list of items
    """
    
    k, varr = arr[0],  list(filter(None,*arr[1:]))
    if not k:
        return False

    return k in varr


def str_to_date(str):
    """
        TODO : 431972 or 04031972 or 04/3/1972 or 4/3/1972 or 4/03/1972 -> Date (24,3,1972)
             then compare dates.. dont have to get to-ordinal
    """
    pass


def get_date_converter(sample_date_str):
    """
    Converts date strings to ordinal integers
    """
    if sample_date_str.find('/') == -1:
        # if date_str.find('/') != -1: # 1/1/2019
        return lambda date_str: datetime.strptime(date_str,"%d%m%Y").toordinal()
    else:
        return lambda date_str: datetime.strptime(date_str,"%d/%m/%Y").toordinal()

# def get_datestring_from_date(date, dtformat='%d%m%Y'):
#     return date.strftime(dtformat)

def get_datestring_from_ordinal(ordinal_date, dtformat='%d%m%Y'):
    return datetime.fromordinal(ordinal_date).strftime(dtformat)

def now_string():
    return datetime.now().strftime('%Y-%m-%d-%H-%M')


def get_latest_data_file(dir='input'):
    import glob
    
    list_of_files = glob.glob(os.path.join(dir,'*.csv')) # * means all if need specific format then *.csv
    return max(list_of_files, key=os.path.getctime)


def get_result_filename(fullname, all_eps=True):
    if not all_eps:
        output_fname_tags ='(closed_eps)'
    else:
        output_fname_tags = '(with_open_eps)'
    
    base = os.path.basename(fullname)
    input_filename = os.path.splitext(base)[0]
    return os.path.join("output", f"./{input_filename}_{output_fname_tags}")
