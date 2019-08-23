from collections import OrderedDict
from datetime import datetime
import re

alpha_pattern = re.compile(r'[\W_0-9]+')
cleanse_string = lambda string: alpha_pattern.sub('', string)

no_unicode_pattern = re.compile(r'[^\x00-\x7F]+')
remove_unicode = lambda string: no_unicode_pattern.sub('', string)

NOW = datetime.now()

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

    
'''
Converts date strings to ordinal integers
'''
def get_date_converter(sample_date_str):
    
    #date_format = None    datetime.fromordinal()
    if sample_date_str.find('/') == -1:
        #date_format = "%d%m%Y"
        # if date_str.find('/') != -1: # 1/1/2019
        return lambda date_str: datetime.strptime(date_str,"%d%m%Y").toordinal()
    else:
        #date_format = "%d/%m/%Y"
        return lambda date_str: datetime.strptime(date_str,"%d/%m/%Y").toordinal()

# def get_datestring_from_date(date, dtformat='%d%m%Y'):
#     return date.strftime(dtformat)

def get_datestring_from_ordinal(ordinal_date, dtformat='%d%m%Y'):
    return datetime.fromordinal(ordinal_date).strftime(dtformat)

def now_string():
    return datetime.now().strftime('%Y-%m-%d-%H-%M')
