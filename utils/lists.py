
# from collections import OrderedDict

# def get_fields_value_string(data):
#     data = OrderedDict(data)

#     data_values_list = list(data.values())
#     value_format = (' %s,' * len(data_values_list)).rstrip(',')

#     fields = ','.join(data.keys())
#     return fields, value_format, data_values_list

    
def has_duplicate_values(*arr) -> bool:
    """
    Checks if the first value in the passed-in list, appears in the rest of the list
    The 2nd item in the passed-in list is a list of items
    """
    
    k, varr = arr[0],  list(filter(None,*arr[1:]))
    if not k:
        return False

    return k in varr

"""
  if val is None, it searches for (and returns) the first index of a None
    if not found return -1
    
  otherwise it searches for (and returns) the first index of a non-None
    if not found return -1

"""

def _first_index_of(*arr, val=None)-> int:
  try:
    if not val and arr:
      #return next(i for i, item in enumerate(arr) if not item)
      for i, item in enumerate(arr):
        if not item:
          return i
    else:
      #return next(i for i, item in enumerate(arr) if item)
      for i, item in enumerate(arr):
        if item:
          return i      
  except ValueError:
    return -1

  return -1


def has_gaps(*arr) -> bool:
  # 1. find first non-blank
  blank_index = _first_index_of(*arr)
  
  if -1 < blank_index < len(arr)-1:
    # 2. if there is a real value (non-blank) in the remainder of the list, then there was a gap
    if _first_index_of(*arr[blank_index+1:], val='any-Non-Blank') >  -1:
      return True
  
  return False



def isin_dicts_array(dct: dict, dict_key: str, search_item:str) -> bool:

  if dict_key in dct:
    found = search_item in dct[dict_key]
    return found

  return False
