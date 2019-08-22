import json
from datetime import date

import jsonschema as jsc
from json_logic import add_operation, jsonLogic
from helpers import (add_error_obj, check_overlap, compile_logic_errors,
                     fix_check_dates, fuse_suggestions_into_errors, getSLK,
                     remove_vrules, translate_to_MDS_header,
                     translate_to_MDS_values)
from MDS_constants import MDS, MDS_Dates
from MDS_RULES import rule_definitions
from MJValidationError import MJValidationError
from utils import NOW, cleanse_string, get_date_converter, has_duplicate_values

rules = [r['rule'] for r in rule_definitions]

st_fld = 'O'+MDS['COMM_DATE']
end_fld = 'O'+MDS['END_DATE']
NOW_ORD = NOW.toordinal()

'''
Create a validation error object with the data row index, client id and error details.
'''
header_er_lam = lambda field, miss_extra: MJValidationError(index='all',
                                    cid='all',
                                    etype='field',
                                    field=field,
                                    message=miss_extra)


class JSONValidator(object):

    def __init__(self, schema_dir, schema_file_name):        
        self.validator, self.schema = JSONValidator.setup_validator(
                                                    schema_dir, schema_file_name)
        self.slk_suggestions = {}


    @staticmethod
    def setup_validator(schema_dir, schema_file_name):
        validator = None
        with open(schema_file_name) as schemaFile:
            schemaObj = json.load(schemaFile)
            resolver = jsc.RefResolver('file:///' + schema_dir, schemaObj)
            validator = jsc.Draft4Validator(schemaObj, resolver=resolver)

        return validator, schemaObj


    # TODO : schema validation may have already deduced that dates, etc may be invalid.
    #        those errors  would contain the rec_index of the error too
    @staticmethod
    def validate_logic(errors, data_row, rec_idx, fn_date_converter,
                       id_field, client_eps):
        """
        1. Checks the date format and converts dates into integer ('ordinal's) for easy comparison.
        2. Checks MDS business logic defined in MDS_RULES.py (and imported in the global 'rule_definitions').
            For example EPISODEs OVERLAP.(See 'ACT MDS Data Collection Guide' document for suggested logic checks)

        3. If there errors in the date formats, all the logic checks (for the passed-in data row),
            that involve the malformed dates are excluded.
           The errors from these validations are added to the 'errors' array that is passed in.

        4. client_eps : This is an (on-going) accumulated list of the start and end dates of the
            passed-in client's episodes. This allows us to calculate episode overlaps with the current data row.
        """
        date_conversion_errors = fix_check_dates(data_row, rec_idx, fn_date_converter,
                                                 id_field, MDS_Dates)
        temp_rd =  rule_definitions
        temp_rules = rules
        dce_fields = []
        if any(date_conversion_errors):
            dce_fields = [dce['field'] for dce in date_conversion_errors]
            temp_rd = remove_vrules(dce_fields)
            temp_rules = [rd['rule'] for rd in temp_rd]
        
        #try: 
        result = [] 
        for r in temp_rules :
            rr = jsonLogic(r, data_row)
            result.append(rr)
        
        #except TypeError:
        #    print(f"type erropr index: {rec_idx}  \t", data_row)
        
        logic_errors = compile_logic_errors(result, temp_rd, data_row,
                                             rec_idx, id_field, date_conversion_errors) 
        if rec_idx not in errors:
            errors[rec_idx] = logic_errors
        elif logic_errors:
            errors[rec_idx].extend(logic_errors)

        # 'OCommencement Date' is a made-up field that contains the ordinal version of the date
        #  to be used for easy comparison (overlap).
        if not ((MDS['COMM_DATE'] in dce_fields) or (MDS['END_DATE'] in dce_fields)):
            cid = data_row[id_field]            
            ep_dates_obj = { st_fld: data_row[st_fld],
                             MDS['COMM_DATE']: data_row[MDS['COMM_DATE']], 
                             'idx': rec_idx }
            if end_fld in data_row:
                ep_dates_obj[end_fld] = data_row[end_fld]
                ep_dates_obj[MDS['END_DATE']] = data_row[MDS['END_DATE']]

            else: #end date is blank, use current date  as end date to check overlap ?
                ep_dates_obj[end_fld] = NOW_ORD
                ep_dates_obj[MDS['END_DATE']] = NOW

            if (cid in client_eps): # any(client_eps.get(cid, [])):
                client_eps[cid].append(ep_dates_obj)
                check_overlap(data_row, client_eps[cid], errors, rec_idx, st_fld=st_fld, end_fld=end_fld)
            else:
                client_eps[cid] = [ep_dates_obj]


        # return compile_logic_errors(result, data_row, rec_idx, id_field, date_conversion_errors) 
    def validate_header(self, header, mode=0):
        warnings = None
        tr_header = [h for h in header]
        if mode == 0:
            tr_header, warnings = translate_to_MDS_header(tr_header)

        schema_headers = set(self.schema['definitions']['episode']['required'])
        missing_headers = schema_headers.difference(set(tr_header))

        return [header_er_lam(field=mh, miss_extra='missing field') for mh in missing_headers], tr_header, warnings


    # TODO : convert everything to MDS codes first to check numeric values (faster). failed lookups are automatically errors
    def validate(self, data, mode=0):
        """
            The main validator function.
            0. If column headers, dropdown values are not proper MDS values, 
                it looks up a translation dictionary and converts them
            1. If dates (DOB, episode start, end) are not proper dates, it logs ERRORs and 
                excludes the logic validation checks that involve those fields.
            2. Does schema validation using the schema specified in JSON files (schema folder).
            3. Does MDS Logic validation using MDS_RULES.py (jsonLogic)
        """
        warnings = {}
        errors = {}
        episodes = data['episodes']
        id_field = MDS['ID']
        if mode == 0: # withouth the deep copy of episodes
            warnings = translate_to_MDS_values(episodes)# translate to official MDS values
            data = {'episodes': episodes}

        for e in self.validator.iter_errors(data):
            add_error_obj(errors, e, data, id_field)
        
        fn_date_converter = get_date_converter(sample_date_str=episodes[0][MDS_Dates[0]])
        add_operation('has_duplicate_values', has_duplicate_values)
        add_operation('check_slk', self.check_slk)

        client_eps = {}
        for i, ep_data in enumerate(episodes):
            JSONValidator.validate_logic(errors, ep_data, i, fn_date_converter,
                                         id_field, client_eps)
        if self.slk_suggestions:
            fuse_suggestions_into_errors(errors, self.slk_suggestions)

        return errors , warnings
 
    
    def check_slk(self, id, data_slk, firstname, lastname, DOB_str, sex_str):
        must_be = getSLK(firstname, lastname, DOB_str, sex_str)

        if data_slk != must_be:
            self.slk_suggestions[id] = must_be
            return False

        return True
