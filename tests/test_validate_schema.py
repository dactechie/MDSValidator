import os
import pytest
from ..MDS_constants import MDS as M, MDS_Dates as D
from ..JSONValidator import JSONValidator

# @pytest.fixture(scope='session')
# def headers_map():
#     # alias_lower -> Officla MDS name
    
#     # k (official name) : v [] -> array of aliases or accepted values
#     return {
#         "Client ID" : "ID",
#         "PID" : "ID",
#         "Method of use for PDC" : "Method of use for principal drug of concern"
#     }

@pytest.fixture(scope='session')
def json_validator():
    # dir = os.path.join(os.getcwd(), os.pardir, 'schema/')
    schema_dir = os.path.join(os.path.dirname( __file__ ), os.pardir , 'schema/')
    schema_file_name = os.path.realpath(os.path.join(schema_dir, 'schema.json'))
    return JSONValidator(schema_dir, schema_file_name)

    # input = [{'ENROLLING PROVIDER':'Tim Ireson'},{'PAT ID':'11525'},{'FULL NAME':'SILBY, JAYDEN'},{'EID':'820002000'},{'SLK581':'ILYAY111219961'},
    #         {'DOB':'35410'},{'SEX':'Male'},{'AGE':'22'},{'DOB ACCURACY':'AAA'},{'COUNTRY':'Australia'},{'INDIG STATUS':'Neither Aboriginal nor TSI'},
    #         {'LANGUAGE':'English'},{'CLIENT':'Own alcohol or other drug use'},{'SOURCE':'Self'},{'ENROLMENT':'43500'},{'DISCHARGE':''},
    #         {'DAYS ENROLLED':''},{'CESSATION':''},{'SETTING':'Non-residential Facility'},{'USE':'Sniffs (powder)'},{'INJECTION':'Never injected'},
    #         {'DRUG':'Cocaine'},{'ODC1':''},{'ODC2':''},{'ODC3':''},{'ODC4':''},{'ODC5':''},{'TREAT':'Counselling'},{'OTT1':''},{'OTT2':''},{'OTT3':''},
    #         {'OTT4':''},{'OTT5':''},{'POSTCODE':'2906'},{'LIVING':'Alone'},{'ACCOM':'Private Residence'},{'PREVIOUS TREATMENT':'No treatment'},
    #         {'MENTAL HEALTH':'Never been diagnosed'},{'DIAGNOSIS':''},{'ARCADIA':''},{'TREATED IN':''},{'PROGRAM':'Counselling and Case Management'}]
MDS = {
    "ID": "ID",
    "SEX": "Sex",
    "COMM_DATE" : "Commencement date",
    "DOB" : 'DOB', #Date of Birth",
    "SLK": "SLK 581",
    "FNAME": "First name",
    "LNAME": "Surname",
    "DAI": "Date accuracy indicator",
    "END_DATE" : "End date",
    "METHOD" : "Method of use for PDC",
    "PDC" : "Principle drug of concern",
    "INJ_USE" : "Injecting drug use status",
    "CLNT_TYP" : "Client type",
    "COB": "Country of birth",
    "ATSI": "Indigenous status",
    "PLANG": "Preferred language",
    "PCODE": "Postcode (Australian)",
    "MTT": "Main treatment type",
    "LIVAR": "Living arrangements",
    "USACC": "Usual accommodation",
    "TRDLVSTG": "Treatment delivery setting",
    "SRC_REF": "Source of referral",
    "MENT_HEL": "Mental health",
    "PREV_AOD": "Previous alcohol and other drug treatment received", #Previous AOD treatment",
    "REAS_CESS": "Reason for cessation"
}

MDS_Dates = ["DOB", "COMM_DATE", "END_DATE"]
def test_sample(json_validator):
    input = [{'ENROLLING PROVIDER':'Tim Ireson'},{'ID':'11525'},{M['FNAME']:'JAYDEN'}, {M['LNAME']: 'SILBY'},{'EID':'820002000'},{M['SLK']:'ILYAY111219961'},
            {'DOB':'35410'},{M['SEX']:'Male'},{'AGE':'22'},{'DAI':'AAA'},{M['COB']:'Australia'},{M['ATSI']:'Neither Aboriginal nor TSI'},
            {M['PLANG']:'English'}, {M['CLNT_TYP']:'Own alcohol or other drug use'},{M['SRC_REF']:'Self'},{D[0]:'43500'},{D[1]:''},
            {'DAYS ENROLLED':''},{M['REAS_CESS']:''},{M['TRDLVSTG']:'Non-residential Facility'},{M['METHOD']:'Sniffs (powder)'},{M['INJ_USE']:'Never injected'},
            {M['PDC']:'Cocaine'},{'ODC1':''},{'ODC2':''},{'ODC3':''},{'ODC4':''},{'ODC5':''},{M['MTT']:'Counselling'},{'OTT1':''},{'OTT2':''},{'OTT3':''},
            {'OTT4':''},{'OTT5':''},{M['PCODE']:'2906'},{M['LIVAR']:'Alone'},{M['USACC']:'Private Residence'},{M['PREV_AOD']:'No treatment'},
            {M['MENT_HEL']:'Never been diagnosed'},{'DIAGNOSIS':''},{'ARCADIA':''},{'TREATED IN':''},{'PROGRAM':'Counselling and Case Management'}]

    result = json_validator.validate({'episodes' :input})

    print(result)