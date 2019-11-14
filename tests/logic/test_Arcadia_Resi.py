
#import os
#from datetime import datetime as dt
import pytest
import copy
#from  ...AOD_MDS.constants import MDS as M, MDS_Dates as D
from ... import schema_dir, schema_file_name
from . import start_period, end_period, JSONValidator, noerrors_base, noerrors_base_translated


@pytest.fixture(scope='module')
def Arcadia_Resi_json_validator():
    start_end = {'start': start_period, 'end': end_period }
    return JSONValidator(schema_dir, schema_file_name, start_end, program='Arcadia-Resi')


def test_Arcadia_Resi(Arcadia_Resi_json_validator):
  #f"If {M['TRDLVSTG']} is Residential treatment', '{M['MTT']}' has to be Withdrawal Mgmt.(Detox) / Rehab."
          # Team-based logic: Treatment Delivery Setting

  base5error = copy.deepcopy(noerrors_base_translated)
  base5error['Treatment delivery setting'] ='Residential treatment facility'
  base5error['ID'] ='7777'
  input = [base5error]

  errors_arcadia, _ = Arcadia_Resi_json_validator.validate({'episodes' :input})

  expected4 = [
      # {'cid':'4353','etype':'logic','field':'Treatment delivery setting','index': 0,
      # 'message': "TSS team does not provide service (treatment delivery) in Home/'Other' setting "
      # },
      {'cid':'7777','etype':'logic','field':'Treatment delivery setting','index': 0,
      'message':  "If Treatment delivery setting is Residential treatment', 'Main treatment type' has to be Withdrawal Mgmt.(Detox) / Rehab."
      }
  ]

  assert errors_arcadia[0] == expected4