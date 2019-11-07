import json
from datetime import date
import jsonschema as jsc

from json_logic import add_operation, jsonLogic
from AOD_MDS.helpers import (add_error_obj, prep_and_check_overlap, 
                        compile_logic_errors, fix_check_dates, 
                        fuse_suggestions_into_errors, getSLK,
                        remove_vrules, translate_to_MDS_header,
                        translate_to_MDS_values, is_valid_drug_use)#, can_process_withdates)
from AOD_MDS.constants import MDS, MDS_Dates, MDS_ST_FLD, MDS_END_FLD
from AOD_MDS.logic_rules.common import rule_definitions as common_rules
from utils import cleanse_string, get_date_converter, has_duplicate_values, has_gaps
from .MJValidationError import MJValidationError
from .constants import MODE_LOOSE, NOW_ORD, NOW

'''
Create a validation error object with the data row index, client id and error details.
'''
header_er_lam = lambda field, miss_extra: MJValidationError(index='all',
                                    cid='all',
                                    etype='field',
                                    field=field,
                                    message=miss_extra)


class JSONValidator(object):
    
    rule_definitions = common_rules
    rules = [r['rule'] for r in rule_definitions]

    def __init__(self, schema_dir, schema_file_name, start_end, program):
        self.validator, self.schema = JSONValidator.setup_validator(
                                                    schema_dir, schema_file_name)
        self.start_end = start_end                                                      
        
        if program != '':
          if program =='TSS': # TODO if there are other specialized (program) rules, make this more dynamic
            from AOD_MDS.logic_rules.TSS import rule_definitions as addnl_def
          elif program ==  'Arcadia-Resi':
            from AOD_MDS.logic_rules.Arcadia_Resi import rule_definitions as addnl_def
          JSONValidator.rule_definitions.extend(addnl_def)
          JSONValidator.rules.extend([r['rule'] for r in addnl_def])

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
    def validate_logic(errors, data_row, rec_idx, date_conversion_errors,
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

        temp_rd =  JSONValidator.rule_definitions
        temp_rules = JSONValidator.rules
        dce_fields = []
        if any(date_conversion_errors):
            dce_fields = [dce['field'] for dce in date_conversion_errors]
            temp_rd = remove_vrules(dce_fields)
            temp_rules = [rd['rule'] for rd in temp_rd]
        
        result = (jsonLogic(r, data_row) for r in temp_rules)
        
        logic_errors = compile_logic_errors(result, temp_rd, data_row,
                                             rec_idx, id_field, date_conversion_errors) 
        if rec_idx not in errors:
            errors[rec_idx] = logic_errors
        elif logic_errors:
            errors[rec_idx].extend(logic_errors)
        
        prep_and_check_overlap(data_row, client_eps, errors, rec_idx, dce_fields)

        # 'OCommencement Date' is a made-up field that contains the ordinal version of the date
        #  to be used for easy comparison (overlap).

        # if there was no error in the commencement and end dates
        # prep_overlap



        # return compile_logic_errors(result, data_row, rec_idx, id_field, date_conversion_errors) 
    def validate_header(self, header, mode=MODE_LOOSE):
        warnings = None
        tr_header = [h for h in header]
        if mode == MODE_LOOSE:
            tr_header, warnings = translate_to_MDS_header(tr_header)

        schema_headers = set(self.schema['definitions']['episode']['required'])
        missing_headers = schema_headers.difference(set(tr_header))

        return [header_er_lam(field=mh, miss_extra='missing field') 
                for mh in missing_headers], tr_header, warnings


    # TODO : convert everything to MDS codes first to check numeric values (faster). failed lookups are automatically errors
    def validate(self, data, mode=MODE_LOOSE):
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

        if mode == MODE_LOOSE: # withouth the deep copy of episodes
            warnings = translate_to_MDS_values(episodes)# translate to official MDS values
            data = {'episodes': episodes}

        for e in self.validator.iter_errors(data):
            add_error_obj(errors, e, data, id_field)

        fn_date_converter = get_date_converter(sample_date_str=episodes[0][MDS_Dates[0]])

        add_operation('has_duplicate_values', has_duplicate_values)
        add_operation('check_slk', self.check_slk)
        add_operation('has_blanks_in_otherdrugs', has_gaps)
        add_operation('is_valid_drug_use', is_valid_drug_use)
        #add_operation('is_outside_period', )
        # if not can_process_withdates(period_st_ed, ep_data[MDS_ST_FLD], ep_data[MDS_END_FLD]
        #                       ,date_conversion_errors, open_and_closed_eps=False): # all_eps              
            
        client_eps = {}
        # stdate = MDS['COMM_DATE']
        # enddate = MDS['END_DATE']
        
        # period_st_ed = { 'start': self.start_end['start'].toordinal(),
        #                  'end' :  self.start_end['end'].toordinal()
        #                 }
     
        for i, ep_data in enumerate(episodes):
            date_conversion_errors = fix_check_dates(ep_data, i, fn_date_converter,
                                                     id_field, MDS_Dates)                                                     
  
            # ep_data[stdate] =str(ep_data[stdate])
            # ep_data[enddate] =str(ep_data[enddate])
            # ep_data[MDS['DOB']] =str(ep_data[MDS['DOB']])
            #print(ep_data)
            JSONValidator.validate_logic(errors, ep_data, i, date_conversion_errors,
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


    def check_age(self):
        """
            TODO : Make sure the age is not < 10
        """
        pass