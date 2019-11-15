
#import os
#from datetime import datetime as dt
import pytest
import copy
#from  ...AOD_MDS.constants import MDS as M, MDS_Dates as D
from MDSValidator import schema_dir, schema_file_name
#from ... import schema_dir, schema_file_name
from . import start_period, end_period, JSONValidator, noerrors_base, noerrors_base_translated


@pytest.fixture(scope='module')
def TSS_json_validator():

    start_end = {'start': start_period, 'end': end_period }
    return JSONValidator(schema_dir, schema_file_name, start_end, program='TSS')



def test_TSS(TSS_json_validator):
        
        base1error = copy.deepcopy(noerrors_base_translated)
        base1error['Treatment delivery setting'] = 'Home'
        base1error['ID'] ='11525'

        base2error = copy.deepcopy(noerrors_base_translated)
        base2error['Main treatment type'] = 'Withdrawal management (detoxification)'
        base2error['Usual accommodation'] = 'Prison/remand centre/youth training centre'
        base2error['Treatment delivery setting'] = 'Non-residential treatment facility'
        base2error['ID'] ='9999'

        base3error = copy.deepcopy(noerrors_base_translated)
        base3error['Usual accommodation'] = 'Prison/remand centre/youth training centre'
        base3error['Treatment delivery setting'] ='Home'
        base3error['ID'] ='1111'
        

        # Team-based logic: Treatment Delivery Setting
        base4error = copy.deepcopy(noerrors_base_translated)
        base4error['Treatment delivery setting'] ='Residential treatment facility'
        base4error['ID'] ='4353'
        input = [base1error, base2error, base3error, base4error]

        errors, _ = TSS_json_validator.validate({'episodes' :input})
                
        expected0 = [

            {'cid': '11525',
            'etype': 'logic',
            'field': 'Treatment delivery setting',
            'index': 0,
            'message': 'TSS team does not provide service (treatment delivery) in '
                      "Home/'Other'/Resi setting "
            }
          ]
        expected1 = [
          {'cid': '9999', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 1, 
            'message': "If Usual accommodation is 'Prison/remand centre/youth training centre', 'Treatment delivery setting' has to be 'Outreach setting'."}, 
          {'cid': '9999', 'etype': 'logic', 'field': 'Main treatment type', 'index': 1, 
            'message': 'TSS team only does the following treatment types: Counselling, Support and case management and Information and education'}     
        ]
        assert errors[0] == expected0
        assert errors[1] == expected1

        expected2 = [
            {'cid':'1111','etype':'logic','field':'Treatment delivery setting','index': 2,
            'message': "If Usual accommodation is 'Prison/remand centre/youth training "
                      "centre', 'Treatment delivery setting' has to be 'Outreach setting'."
            },
            {'cid': '1111','etype': 'logic','field': 'Treatment delivery setting','index': 2,
            'message': 'TSS team does not provide service (treatment delivery) in '
                        "Home/'Other'/Resi setting "
            },
        ]
        assert errors[2] == expected2

        expected3 = [
            {'cid':'4353','etype':'logic','field':'Treatment delivery setting','index': 3,
            'message': "TSS team does not provide service (treatment delivery) in Home/'Other'/Resi setting "
            }
        ]
        assert errors[3] == expected3




# 0: [{'cid': '11525', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 0, 'message': "TSS team does not provide service (treatment delivery) in Home/'Other'/Resi setting "}]
# 1: [{'cid': '9999', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 1, 'message': "If Usual accommodation is 'Prison/remand centre/youth training centre', 'Treatment delivery setting' has to be 'Outreach setting'."}, 
#     {'cid': '9999', 'etype': 'logic', 'field': 'Main treatment type', 'index': 1, 'message': 'TSS team only does the following treatment types: Counselling, Support and case management and Information and education'}]
# 2: [{'cid': '1111', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 2, 'message': "If Usual accommodation is 'Prison/remand centre/youth training centre', 'Treatment delivery setting' has to be 'Outreach setting'."}, 
#   {'cid': '1111', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 2, 'message': "TSS team does not provide service (treatment delivery) in Home/'Other'/Resi setting "}]
# 3: [{'cid': '4353', 'etype': 'logic', 'field': 'Treatment delivery setting', 'index': 3, 'message': "TSS team does not provide service (treatment delivery) in Home/'Other'/Resi setting "}]
