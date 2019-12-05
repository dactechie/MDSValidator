
#import os
#from datetime import datetime as dt
import pytest
import copy
from ...AOD_MDS.constants import MDS as M
from MDSValidator import schema_dir, schema_file_name
from . import  JSONValidator, noerrors_base, noerrors_base_translated, S_PRISON_OUTR, period

S_MTT_PHARM = "If MTT is Pharmacotherapy, OTT1 should be present"
ex_tds = { 'etype': 'logic', 'field': M['MTT']}
error = { 'index': 0 ,'cid': '',  **ex_tds, 'message': S_MTT_PHARM}


@pytest.fixture(scope="module")
def Althea_json_validator():
    return JSONValidator(schema_dir, schema_file_name, period=period, program='Althea')


@pytest.mark.parametrize("client_id, mtt, ott1, err", [
                                           ('11525',  'Support and case management', '', {}),
                                            ('4353', 'Information and education', '', {}),
                                           ('343','Pharmacotherapy', '', error),
                                            ('11525','Pharmacotherapy', 'Support and case management', {}),
                                            ('11525','Support and case management', 'Pharmacotherapy', {}),
                                          ])
def test_no_treat_resi(Althea_json_validator, client_id, mtt, ott1, err):
  base1_error = copy.deepcopy(noerrors_base_translated)
  base1_error[M['MTT']] =  mtt
  base1_error['OTT1'] =  ott1
  base1_error['ID'] = client_id

  if err:
    err['cid'] = client_id
  
  errors, _ = Althea_json_validator.validate({'episodes' :[base1_error]})
  
  assert (not err and len(errors[0]) == 0) or errors[0][0] == err


