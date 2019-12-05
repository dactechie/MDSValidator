#import os
import pytest
import pytest_dependency
import copy
#from AOD_MDS.constants import MDS as M, MDS_Dates as D


from collections import OrderedDict
from  MDSValidator import schema_dir, schema_file_name

#from  MDSValidator.rule_checker import  
from . import JSONValidator, noerrors_base, noerrors_base_translated, period


@pytest.fixture(scope="module")
def json_validator():    
    return JSONValidator(schema_dir, schema_file_name, period=period, program=None)


@pytest.mark.dependency() 
def test_header_noerrors(json_validator):
  header = list(noerrors_base)
  missing_headers, fixed_header, header_warnings = json_validator.validate_header(header, mode=False)
  expected_header = ['ID','First name','Surname','SLK 581','DOB','Sex','Date accuracy indicator','Country of birth','Indigenous status','Preferred language',
    'Client type','Source of referral','Commencement date','End date','Reason for cessation','Treatment delivery setting','Method of use for PDC',
    'Injecting drug use status','Principle drug of concern','ODC1','ODC2','ODC3','ODC4','ODC5','Main treatment type','OTT1','OTT2','OTT3','OTT4',
    'Postcode (Australian)','Living arrangements','Usual accommodation','Previous alcohol and other drug treatment received','Mental health']


  assert expected_header == fixed_header
  assert OrderedDict({'ACCOM':'Usual accommodation', 'CESSATION':'Reason for cessation', 'CLIENT':'Client type',
                      'COUNTRY':'Country of birth', 'DISCHARGE':'End date', 'DOB ACCURACY':'Date accuracy indicator',
                      'DRUG':'Principle drug of concern', 'ENROLMENT':'Commencement date', 'INDIG STATUS':'Indigenous status',
                      'INJECTION':'Injecting drug use status', 'LANGUAGE':'Preferred language', 'LIVING':'Living arrangements',
                      'MENTAL HEALTH':'Mental health', 'PAT ID':'ID', 'POSTCODE':'Postcode (Australian)',
                      'PREVIOUS TREATMENT':'Previous alcohol and other drug treatment received', 'SETTING':'Treatment delivery setting',
                      'SEX':'Sex', 'SLK581':'SLK 581', 'SOURCE':'Source of referral', 'TREAT':'Main treatment type',
                      'USE':'Method of use for PDC'}).items() ==  header_warnings.items()

  assert len(missing_headers) == 0, "the list is not empty" # empty list



@pytest.mark.dependency(depends=["test_header_noerrors"])
def test_data_noerrors(json_validator):
        errors, _ = json_validator.validate({'episodes' : [noerrors_base_translated]})
    
        expected = []        
        assert errors[0] == expected


def test_out_of_period(json_validator):
  baseerror = copy.deepcopy(noerrors_base_translated)
  baseerror['Commencement date'] = '01/01/2017'
  baseerror['End date'] ='01/01/2020'
  baseerror['ID'] ='7777'
  input = [baseerror]

  errors, _ = json_validator.validate({'episodes' :input})

  expected4 = [{'cid': '7777',  'etype': 'logic','field': 'End date',
                'index': 0, 'message': 'Episode End Date is not in the reporting period'
                }]

  assert errors[0] == expected4