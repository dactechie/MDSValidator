import copy
import csv

from .aliases import mds_aliases
from .constants import MDS, MDS_END_FLD, MDS_ST_FLD, MDS_Dates
from rule_checker.constants import MODE_LOOSE, NOW, NOW_ORD
from rule_checker.field_lists import (involved_field_sets,
                                      rd_with_involved_fields,
                                      rd_wo_involved_fields)
from utils import (get_23, get_235, cleanse_string,
                         get_datestring_from_ordinal, remove_unicode,
                         isin_dicts_array)
from utils.dates import inperiod, in_period_date
from logger import logger
from AOD_MDS.logic_rules.method_of_use_matrix import drug_usage

'''
Input data file may not have the exact spelling/case as the official MDS fields
list_of_alias_mappings:
    [ { 'DOB' : ['Date of birth', 'DoB'] },
      { 'Principle drug of concern': ['PDC'] }
    ]
We prepare the Alias lookup table here. Result :
    {'Date of birth' : 'DOB',
        'DoB' : 'DOB',
        'PDC' : 'Principle drug of concern'
    }
'''
alias_map_lam = lambda list_of_alias_mappings : { alias: official_name
                                    for official_name, aliases in list_of_alias_mappings.items()
                                    for alias in aliases }


v_er_date_lam = lambda rec_idx, cid, date_field , err_val: {"index":rec_idx,
                                    "cid":cid,
                                    "etype":"date-format",
                                    "field":date_field,
                                    "message":f"Invalid date format {err_val}"}

v_er_lam = lambda rule_i, rules, rec_idx, cid: { "index": rec_idx,
                                    "cid":cid,
                                    "etype":"logic",
                                    "field":rules[rule_i]['field'],
                                    "message":rules[rule_i]['message']}

v_warn_lam = lambda rec_idx, cid, required, got: {
                    "index": rec_idx, "cid":cid, "required": required, "got": got
                    }


headers_map = alias_map_lam(mds_aliases['headers'])
fvalues_map = alias_map_lam(mds_aliases['fieldValues'])
val_translation_excluded_fields = ["ENROLLING PROVIDER", "EID", 
                                   MDS["ID"], MDS["DOB"], MDS["PCODE"], MDS["SLK"] ]


def read_header(filename: str) -> list:
    with open(filename, 'r') as csvfile:
        headers = [header for header in csvfile.readline().split(',')]
        headers[-1] = headers[-1].strip('\n')
        return headers


def is_valid_drug_use(drug_name:str, method_of_use:str) -> bool:
  return isin_dicts_array(drug_usage, drug_name, method_of_use)
  

def can_process_withdates(period_st_ed, ep_start, ep_end, 
                          date_conversion_errors, open_and_closed_eps=False):
  
  error_field = next((dce for dce in date_conversion_errors 
                      if dce['field'] in (MDS_ST_FLD, MDS_END_FLD)), None)
  if error_field:
    logger.error("error in a date field, skipping row  " + error_field)
    return False

  if open_and_closed_eps:
    if not ep_end :
      return in_period_date(period_st_ed, ep_start)
  elif not ep_end: # closed episodes only, but passed-in data had no closed date
    logger.error(f"End date was blank, skipping row . Ep start date: {ep_start}")
    return False
  
  return inperiod(period_st_ed, ep_start, ep_end)
    

def _split_fullname(reader) -> list:
  data_dicts = []
  for i, r in enumerate(reader):
    if  "".join(r.values()) == '':
        logger.error(f"\n\tFound Blank row at {i}. Quitting...")
        return None
    row = copy.deepcopy(r)
    if row.get("FULL NAME"):              
        row[MDS['LNAME']], row[MDS['FNAME']]  = str.split(row["FULL NAME"], ", ")
        del row["FULL NAME"]
    
    data_dicts.append(row)

  return data_dicts

# TODO clean this up (use a generator)
def read_data(filename: str, data_header: dict, hmap: dict, 
                             start_end: dict, all_eps=True) -> dict:
    """
    - Assumes that if a "FULL NAME" column exists, all rows will have a format of
        'LastName, FirstName'.
    - Sometimes the header may have unicode (special) characters, cleans before use.
    - hmap is a map of the header fields with official MDS translations,
        where cleansing was required.
    - all_eps == False => Closed eps only
    """
    #data_header = fix_headers(data_header)
    with open(filename, 'r') as csvfile:
        csvfile.readline()
        reader = csv.DictReader(csvfile, data_header)
        
        if MDS['FNAME'] not in data_header and "FULL NAME" in data_header:
          rows = _split_fullname(reader)           
          reader = rows
          data_header.remove("FULL NAME")
          data_header.extend([MDS['FNAME'], MDS['LNAME']])
        
        clean_headers = {dh: remove_unicode(dh) for dh in data_header}
        # [ch for ch in clean_headers.values() if ch in data_header] == data_header
        # True
        tmp_k = None
        result = []
        ii = 0
        for i, row in enumerate(reader):
            if  "".join(row.values()) == '':
              logger.error(f"\n\tFound Blank row at {i}. skipping to next row...")
              continue

            if not all_eps and not row[MDS['END_DATE']]:
              continue

            result.append({})
            for k, v in row.items():
                tmp_k = clean_headers[k]
                # if tmp_k in hmap:
                #     result[i][hmap[tmp_k]] = v
                # else:
                result[ii][tmp_k] = v
            ii = ii + 1

        #result = [ {k:v for k, v in row.items()} for row in reader if hmap[k]]
 
        return { "episodes" :result }


# Note: this modifies the original data_row (not a pure function)
def fix_check_dates(data_row, rec_idx, fn_date_converter,
                    id_field, date_fields) -> list:
    k = None
    date_conversion_errors = []
    
    for d in date_fields:
        k = MDS[d]
        dt = data_row[k]
        if not dt: #and not expect_all: # end date might be blank, nothing to convert : 
                                      # FIXME: above is not true, might have overlapping open episodes
            continue
        l = len(dt)
        # if l < 7:
        #     logger.warn(f"Warning : invalid date string {dt}. Not converting to Date.")
        #     continue
        if l == 7 or dt.find('/') == 1 : #no leading zero in the case of 1_01_1981 or 1/01/1981
            dt = '0' + dt
            data_row[k] = dt
        try:
            data_row['O'+k] = fn_date_converter(dt)
        except ValueError :#as e:
            date_conversion_errors.append(v_er_date_lam(rec_idx, data_row[id_field], k, dt))

    return date_conversion_errors


def translate_to_MDS_header(header):
    warnings = {}
    converted_header = copy.deepcopy(header)# [cleanse_string(h) for h in header]

    for i, h in enumerate(header):
        hlow = h#.lower()
        if hlow in headers_map:    # {alias1 : official_k1}, {alias2 : official_k1}, ...
            converted_header[i] = headers_map[hlow] #save the official MDS value in the new header
            warnings[h] = headers_map[hlow]
            #warnings[f"Header uses key:{h} instead of {headers_map[hlow]}"] = 1

    return converted_header, warnings
 

#without the deep copy
def translate_to_MDS_values(data):
    warnings = []
    fields_to_check = [k for k in data[0] if k not in val_translation_excluded_fields]

    for i, ddict in enumerate(data):# each row                          [ {row1}, {row2}  {ID: 2}]
        #for data_key, v in ddict.items(): # each field within a row     row1->  { k1:v1 , k2:v2} 
        for data_key in fields_to_check:
            v =  ddict[data_key]
            conv_data_val = v.strip()
            if conv_data_val in fvalues_map:
                conv_data_val = fvalues_map[conv_data_val]
                warnings.append (
                        v_warn_lam(i,ddict[MDS['ID']],conv_data_val,v)
                    )
            data[i][data_key] = conv_data_val

    return warnings
    

def remove_vrules(error_fields):
    """
        Validation for fields that we already know have errors is pointless.
        Can't (check logic) i.e. do date comparisons, when the dates are not even well-formatted.
        So we remove rules that have dependencies on (involved with) those fields. 
        For now this just means dates.
    """
    error_field_set = set(error_fields)
    new_rd = copy.deepcopy(rd_wo_involved_fields)

    rule_defs_wo_errors = [rd_with_involved_fields[i]
                        for i, inv_fld_set in enumerate(involved_field_sets)
                        if error_field_set.isdisjoint(inv_fld_set)]

    new_rd.extend(rule_defs_wo_errors)

    return new_rd


def prep_and_check_overlap(data_row, client_eps, errors, rec_idx, date_error_fields):
    if not ((MDS['COMM_DATE'] in date_error_fields) 
                              or (MDS['END_DATE'] in date_error_fields)):
        cid = data_row[MDS['ID']]
        ep_dates_obj = { MDS_ST_FLD: data_row[MDS_ST_FLD],
                            MDS['COMM_DATE']: data_row[MDS['COMM_DATE']], 
                            'idx': rec_idx }
        if MDS_END_FLD in data_row:
            ep_dates_obj[MDS_END_FLD] = data_row[MDS_END_FLD]
            ep_dates_obj[MDS['END_DATE']] = data_row[MDS['END_DATE']]

        else: #end date is blank, use current date  as end date to check overlap ?
            ep_dates_obj[MDS_END_FLD] = NOW_ORD
            ep_dates_obj[MDS['END_DATE']] = NOW

        if (cid in client_eps): # any(client_eps.get(cid, [])):
            client_eps[cid].append(ep_dates_obj)
            check_overlap(data_row, client_eps[cid], errors, rec_idx, 
                          st_fld=MDS_ST_FLD, end_fld=MDS_END_FLD)
        else:
            client_eps[cid] = [ep_dates_obj]


"""
  check if the current episode client_eps, overlaps with any previously seen 
  episode for this client.
"""
def check_overlap(current_ep, client_eps, errors, rec_idx,
                  st_fld=MDS["COMM_DATE"], end_fld=MDS["END_DATE"]):

    start_date = client_eps[-1] [st_fld]
    end_date = client_eps[-1][end_fld]

    for ep in client_eps[:-1]:
        if min(end_date, ep[end_fld]) >= max(start_date, ep[st_fld]):
            other_st = get_datestring_from_ordinal(ep[st_fld], dtformat="%d/%m/%Y")
            other_end = get_datestring_from_ordinal(ep[end_fld], dtformat="%d/%m/%Y")

            errors[rec_idx].append( { 'index': rec_idx,
                                    'cid': current_ep[MDS['ID']],
                                    'etype': 'logic',
                                    'field': MDS['END_DATE'],
                                    'message': \
                f"Overlaps with other episode Start: {other_st} End: {other_end}"
                                    })
            errors[ep['idx']].append( { 'index': ep['idx'],
                                    'cid': current_ep[MDS['ID']],
                                    'etype': 'logic',
                                    'field': MDS['END_DATE'],
                                    'message': \
                f"Overlaps with other episode Start: {ep[MDS['COMM_DATE']]} End: {ep[MDS['END_DATE']]}"
                                    })


def add_error_to_list(error_obj, errors):
    ve_idx = error_obj['index']
    if ve_idx in errors:
        errors[ve_idx].append(error_obj)
    else:
        errors[ve_idx] = [error_obj]


def add_error_obj(errors, e, dataObj, id_field):
    path = e.path
    row = path[1]
    error_obj = {"index": row, "cid": dataObj['episodes'][row][id_field],
                               "etype": e.validator}
    
    if len(path) > 2:
        error_obj["field"]   = path[2]
        error_obj["message"] = f"invalid value/format: '{e.instance}'"
    else:
        error_obj["field"]= '<>'
        if len(e.message) > 50:   # oneOf fields are missing . Not checked as part of header checks
          if len(e.validator_value) > 0 and 'required' in e.validator_value[0]:
            st = e.validator_value[0]['required']        
            error_obj["message"]= f"Missing fields {st}.  row: {error_obj['index']} cid: {error_obj['cid']}"
            add_error_to_list(error_obj, errors)
            return -1
        else:
          error_obj["message"]= e.message

    add_error_to_list(error_obj, errors)
    return 0

        # "oneOf": [
        #   {
        #     "properties": {
        #       "First name":  { "type": "string" }              
        #       }
        #   },
        #   {
        #     "properties": {
        #       "FULL NAME":  { "type": "string" }
        #     }
        #   }
        # ],


def compile_errors(schema_validation_verrors, logic_errors):
    errors = []
    if logic_errors:
        logic_errors = (l for l in logic_errors if l)
        errors =  (item for sublist in logic_errors for item in sublist)
        
    if schema_validation_verrors:
        errors.extend(schema_validation_verrors)

    return errors


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


def compile_logic_errors(result, rule_defs, data_row, rec_idx, id_field, date_conversion_errors):
    # false values means that rule was violated. So we only want the indices of falses :

    idxes = (i for i, r in enumerate(result) if not r)
    
    rule_errors = [v_er_lam(rule_i, rule_defs, rec_idx, data_row[id_field]) for rule_i in idxes]
    if rule_errors: 
        if date_conversion_errors:
            rule_errors.extend(date_conversion_errors)
        return rule_errors

    return date_conversion_errors


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


def log_results(verrors, warnings, header_warnings):
    
    logger.info(f"\n {10*'-'}   Errors {10*'-'}")
    for v in verrors.values():
        logger.info(v)
        logger.info("")

    if any(warnings):
        logger.info(f"\n {10*'-'},  Warnings ,{10*'-'}")
        logger.info(warnings)

    if (header_warnings):
        logger.info(f"\n header warnings {header_warnings}")
