from datetime import datetime
from dateutil.relativedelta import relativedelta


def in_period_date(period: dict, ep_start: datetime) -> bool:
  return ep_start <=  period['end']


def inperiod(period: dict, ep_start: datetime, ep_end: datetime) -> bool:
  return period['start'] <= ep_start <=  ep_end <=  period['end']


def get_period_dict(start_date: datetime, period_months=3) -> datetime :
  end_date =  start_date + relativedelta(months=+period_months) - relativedelta(days=+1)
  return  {'start': start_date, 'end': end_date }


def str_to_date(str):
    """
        TODO : 431972 or 04031972 or 04/3/1972 or 4/3/1972 or 4/03/1972 -> Date (24,3,1972)
             then compare dates.. dont have to get to-ordinal
    """
    pass

## 
#  MJ  4/11/2019  - Ordinal date conversion for jsonLogic ??
def get_date_converter(sample_date_str):
    """
    Converts date strings to ordinal integers
    """
    if sample_date_str.find('/') == -1:
        return lambda date_str: datetime.strptime(date_str,"%d%m%Y").toordinal()
    else:
        return lambda date_str: datetime.strptime(date_str,"%d/%m/%Y").toordinal()

# def get_datestring_from_date(date, dtformat='%d%m%Y'):
#     return date.strftime(dtformat)

def get_datestring_from_ordinal(ordinal_date, dtformat='%d%m%Y'):
    return datetime.fromordinal(ordinal_date).strftime(dtformat)

def now_string():
    return datetime.now().strftime('_%d-%H-%M')
