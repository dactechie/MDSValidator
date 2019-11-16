
#import os
#from datetime import datetime as dt
import pytest
import copy
from MDSValidator import schema_dir, schema_file_name
from . import start_end, JSONValidator, noerrors_base, noerrors_base_translated, S_PRISON_OUTR

S_NOTREAT_RESI = "TSS team does not provide service (treatment delivery) in Home/'Other'/Resi setting "
ex_tds = { 'etype': 'logic', 'field': 'Treatment delivery setting'}

@pytest.fixture(scope="module")
def TSS_json_validator():
    return JSONValidator(schema_dir, schema_file_name, start_end, program='TSS')


@pytest.mark.parametrize("client_id, tds", [('11525',  'Home'),
                                           ('4353', 'Residential treatment facility'),
                                           ('343','Other')
                                          ])
def test_no_treat_resi(TSS_json_validator, client_id, tds):
   base1_error = copy.deepcopy(noerrors_base_translated)
   base1_error['Treatment delivery setting'] =  tds
   base1_error['ID'] = client_id

   errors, _ = TSS_json_validator.validate({'episodes' :[base1_error]})
   assert errors[0] == [{ 'index': 0 ,'cid': client_id,  **ex_tds, 'message': S_NOTREAT_RESI}]


def test_tds_good(TSS_json_validator):
        # Team-based logic: Treatment Delivery Setting
        base4error = copy.deepcopy(noerrors_base_translated)
        base4error['Treatment delivery setting'] ='Non-residential treatment facility'
        base4error['ID'] ='4353'
        
        errors, _ = TSS_json_validator.validate({'episodes' :[base4error]})
        assert errors[0] == []



def test_jailoutreach_mttallowed(TSS_json_validator):

        jail_input = {**noerrors_base_translated,
            'Usual accommodation' : 'Prison/remand centre/youth training centre'}

        base0error = jail_input.copy()        
        base0error['Treatment delivery setting'] ='Home'
        base0error['ID'] ='1111'
        
        expected0 = [
            {'cid':'1111',**ex_tds,'index': 0, 'message': S_PRISON_OUTR },
            {'cid':'1111',**ex_tds,'index': 0, 'message': S_NOTREAT_RESI },
        ]

        base1error = jail_input.copy()
        base1error['Main treatment type'] = 'Withdrawal management (detoxification)'
        base1error['Treatment delivery setting'] = 'Non-residential treatment facility'
        base1error['ID'] ='9999'

        expected1 = [{'cid': '9999', **ex_tds,'index': 1, 'message': S_PRISON_OUTR}, 
          {'cid': '9999', 'etype': 'logic', 'field': 'Main treatment type', 'index': 1,
            'message': 'TSS team only does the following treatment types: Counselling, Support and case management and Information and education'}     
        ]

        errors, _ = TSS_json_validator.validate({'episodes' :[base0error, base1error]})
                        
        assert errors[0] == expected0
        assert errors[1] == expected1
