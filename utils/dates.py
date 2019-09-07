from datetime import datetime

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
