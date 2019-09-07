
# from collections import OrderedDict

# def get_fields_value_string(data):
#     data = OrderedDict(data)

#     data_values_list = list(data.values())
#     value_format = (' %s,' * len(data_values_list)).rstrip(',')

#     fields = ','.join(data.keys())
#     return fields, value_format, data_values_list

    
def has_duplicate_values(*arr):
    """
    Checks if the first value in the passed-in list, appears in the rest of the list
    The 2nd item in the passed-in list is a list of items
    """
    
    k, varr = arr[0],  list(filter(None,*arr[1:]))
    if not k:
        return False

    return k in varr
