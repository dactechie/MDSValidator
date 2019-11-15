from MDSValidator.AOD_MDS.constants import MDS

# from rule_checker.field_lists import (involved_field_sets,
#                                       rd_with_involved_fields,
#                                       rd_wo_involved_fields)
from MDSValidator.utils import isin_dicts_array
#from utils.dates import inperiod, in_period_date
from MDSValidator.logger import logger
from MDSValidator.AOD_MDS.logic_rules.method_of_use_matrix import drug_usage


def is_valid_drug_use(drug_name:str, method_of_use:str) -> bool:
  return isin_dicts_array(drug_usage, drug_name, method_of_use)


def _check_row_errors(array_of_dicts, suggestions, slk_field):
    """
    Note: there could be two rows with same client id, but one of them may have accurate SLK.
    This will added the error to both rows.
    """
    for d in array_of_dicts:
        if d['cid'] in suggestions and d['field'] == slk_field:
            d['message'] = suggestions[d['cid']]
            return


def fuse_suggestions_into_errors(errors, suggestions):
    slk_field = MDS['SLK']
    for array_of_dicts in errors.values():
        _check_row_errors(array_of_dicts, suggestions, slk_field)

# def can_process_withdates(period_st_ed, ep_start, ep_end, 
#                           date_conversion_errors, open_and_closed_eps=False):
  
#   error_field = next((dce for dce in date_conversion_errors 
#                       if dce['field'] in (MDS_ST_FLD, MDS_END_FLD)), None)
#   if error_field:
#     logger.error("error in a date field, skipping row  " + error_field)
#     return False

#   if open_and_closed_eps:
#     if not ep_end :
#       return in_period_date(period_st_ed, ep_start)
#   elif not ep_end: # closed episodes only, but passed-in data had no closed date
#     logger.error(f"End date was blank, skipping row . Ep start date: {ep_start}")
#     return False
  
#   return inperiod(period_st_ed, ep_start, ep_end)