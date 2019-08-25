import os
import pytest
from ..MDS_constants import MDS as M, MDS_Dates as D
from  ..JSONValidator import JSONValidator

# @pytest.fixture(scope='session')
# def headers_map():
#     # alias_lower -> Officla MDS name
    
#     # k (official name) : v [] -> array of aliases or accepted values
#     return 
#         "Client ID" : "ID",
#         "PID" : "ID",
#         "Method of use for PDC" : "Method of use for principal drug of concern"
#     

@pytest.fixture(scope='session')
def json_validator():
    schema_dir = os.path.join(os.path.dirname( __file__ ), os.pardir , 'schema/')
    schema_file_name = os.path.realpath(os.path.join(schema_dir, 'schema.json'))
    return JSONValidator(schema_dir, schema_file_name)

    # input = ['ENROLLING PROVIDER':'Tim Ireson','PAT ID':'11525','FULL NAME':'SILBY, JAYDEN','EID':'820002000','SLK581':'ILYAY111219961',
    #         'DOB':'35410','SEX':'Male','AGE':'22','DOB ACCURACY':'AAA','COUNTRY':'Australia','INDIG STATUS':'Neither Aboriginal nor TSI',
    #         'LANGUAGE':'English','CLIENT':'Own alcohol or other drug use','SOURCE':'Self','ENROLMENT':'43500','DISCHARGE':'',
    #         'DAYS ENROLLED':'','CESSATION':'','SETTING':'Non-residential Facility','USE':'Sniffs (powder)','INJECTION':'Never injected',
    #         'DRUG':'Cocaine','ODC1':'','ODC2':'','ODC3':'','ODC4':'','ODC5':'','TREAT':'Counselling','OTT1':'','OTT2':'','OTT3':'',
    #         'OTT4':'','OTT5':'','POSTCODE':'2906','LIVING':'Alone','ACCOM':'Private Residence','PREVIOUS TREATMENT':'No treatment',
    #         'MENTAL HEALTH':'Never been diagnosed','DIAGNOSIS':'','ARCADIA':'','TREATED IN':'','PROGRAM':'Counselling and Case Management']

#MDS_Dates = ["DOB", "COMM_DATE", "END_DATE"]
def test_sample(json_validator):
        input = [{'ENROLLING PROVIDER': 'Tim Ireson' , 'ID':'11525','FULL NAME':'SILBY, JAYDEN','EID':'820002000','SLK581':'ILYAY111219961',
                'DOB':'3052010','SEX':'Male','AGE':'22',
                'Date accuracy indicator': 'AAA - Day, month and year are accurate', 'Country of birth': 'Australia',
              'Indigenous status': 'Neither Aboriginal nor Torres Strait Islander origin', 
              'Preferred language': 'English', 'Client type': 'Own alcohol or other drug use', 'Source of referral':'Self', 'Commencement date': '4022019', 
              'End date': '', 'DAYS ENROLLED': '', 'Reason for cessation': '', 'Treatment delivery setting': 'Non-residential treatment facility', 
              'Method of use for PDC': 'Sniffs (powder)', 'Injecting drug use status': 'Never injected', 'Principle drug of concern': 'Cocaine', 
              'ODC1': '', 'ODC2': '', 'ODC3': '', 'ODC4': '', 'ODC5': '', 'Main treatment type': 'Counselling', 'OTT1': '', 'OTT2': '', 'OTT3': '',
              'OTT4': '', 'OTT5': '', 'Postcode (Australian)': '2906', 'Living arrangements': 'Alone', 'Usual accommodation': 'Private residence', 
              'Previous alcohol and other drug treatment received': 'No previous treatment received', 'Mental health': 'Never been diagnosed', 'DIAGNOSIS': '', 'ARCADIA': '',
             'TREATED IN': '', 'PROGRAM': 'Counselling and Case Management', 'Surname': 'SILBY', 'First name': 'JAYDEN'}]
    
        # input = [{'ENROLLING PROVIDER':'Tim Ireson',M['ID']:'11525',M['FNAME']:'JAYDEN', M['LNAME']: 'SILBY','EID':'820002000',M['SLK']:'ILYAY111219961',
        #     'DOB':'35410',M['SEX']:'Male','AGE':'22','DAI':'AAA',M['COB']:'Australia',M['ATSI']:'Neither Aboriginal nor TSI',
        #     M['PLANG']:'English', M['CLNT_TYP']:'Own alcohol or other drug use',M['SRC_REF']:'Self',M[D[1]]:'43500',M[D[2]]:'',
        #     'DAYS ENROLLED':'',M['REAS_CESS']:'',M['TRDLVSTG']:'Non-residential Facility',M['METHOD']:'Sniffs (powder)',M['INJ_USE']:'Never injected',
        #     M['PDC']:'Cocaine','ODC1':'','ODC2':'','ODC3':'','ODC4':'','ODC5':'',M['MTT']:'Counselling','OTT1':'','OTT2':'','OTT3':'',
        #     'OTT4':'','OTT5':'',M['PCODE']:'2906',M['LIVAR']:'Alone',M['USACC']:'Private Residence',M['PREV_AOD']:'No treatment',
        #     M['MENT_HEL']:'Never been diagnosed','DIAGNOSIS':'','ARCADIA':'','TREATED IN':'','PROGRAM':'Counselling and Case Management'}]
        errors, warnings = json_validator.validate({'episodes' :input})
        # expected = {0: 
        #                 [   {'index': 0, 'cid': '11525', 'etype': 'required'}, 
        #                     {'index': 0, 'cid': '11525', 'etype': 'date-format', 'field': 'DOB', 'message': 'Invalid date format 35410'}, 
        #                     {'index': 0, 'cid': '11525', 'etype': 'date-format', 'field': 'Commencement date', 'message': 'Invalid date format 43500'}
        #                 ]
        #             }, 
        #         [{'index': 0, 'cid': '11525', 'required': 'AAA - Day, month and year are accurate', 'got': 'AAA'}, 
        #         {'index': 0, 'cid': '11525', 'required': 'Neither Aboriginal nor Torres Strait Islander origin', 'got': 'Neither Aboriginal nor TSI'},
        #         {'index': 0, 'cid': '11525', 'required': 'Non-residential treatment facility', 'got': 'Non-residential Facility'}, 
        #         {'index': 0, 'cid': '11525', 'required': 'Private residence', 'got': 'Private Residence'}, 
        #         {'index': 0, 'cid': '11525', 'required': 'No previous treatment received', 'got': 'No treatment'}]
                
                
        print(errors)
        #print()
        # print()
