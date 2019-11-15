from MDSValidator.rule_checker.JSONValidator import JSONValidator
from datetime import datetime as dt
from collections import OrderedDict

start_period = dt(2018, 7, 1)
end_period = dt(2018, 9, 30)


noerrors_base = OrderedDict(
  {
    "PAT ID": "5119","First name": "NICK","Surname": "ADAMOPOULOS","SLK581": "DAOIC130819851","DOB": "13/08/1985",
    "SEX": "Male","DOB ACCURACY": "AAA","COUNTRY": "Australia","INDIG STATUS": "Neither Aboriginal nor TSI","LANGUAGE": "English",
    "CLIENT": "Own alcohol or other drug use","SOURCE": "Correctional service","ENROLMENT": "9/04/2019","DISCHARGE": "9/12/2019",
    "CESSATION": "","SETTING": "Non-residential Facility","USE": "Smokes","INJECTION": "Never injected",
    "DRUG": "Nicotine","ODC1": "","ODC2": "","ODC3": "","ODC4": "","ODC5": "","TREAT": "Counselling","OTT1": "",
    "OTT2": "","OTT3": "","OTT4": "","OTT5": "","POSTCODE": "2913","LIVING": "Not Stated / Inadequately Described","ACCOM": "Not stated/inadequately described",
    "PREVIOUS TREATMENT": "","MENTAL HEALTH": "Never been diagnosed"
  }
)


noerrors_base_translated = OrderedDict(
  {
    "ID": "5119","First name": "NICK","Surname": "ADAMOPOULOS","SLK 581": "DAOIC130819851","DOB": "13/08/1985",
    "Sex": "Male",'Date accuracy indicator': "AAA",  'Country of birth': "Australia", 'Indigenous status': "Neither Aboriginal nor TSI", 'Preferred language': "English",
    'Client type': "Own alcohol or other drug use", 'Source of referral': "Correctional service", 'Commencement date': "9/04/2019", 'End date': "9/12/2019",
    'Reason for cessation': "", 'Treatment delivery setting': "Non-residential Facility", 'Method of use for PDC': "Smokes",  'Injecting drug use status': "Never injected",
    'Principle drug of concern': "Nicotine","ODC1": "","ODC2": "","ODC3": "","ODC4": "","ODC5": "",'Main treatment type': "Counselling","OTT1": "",
    "OTT2": "","OTT3": "","OTT4": "","OTT5": "", 'Postcode (Australian)': "2913", 'Living arrangements': "Not Stated / Inadequately Described", 'Usual accommodation': "Not stated/inadequately described",
   'Previous alcohol and other drug treatment received': "", 'Mental health': "Never been diagnosed"
  }
)
# PAT ID	First name	Surname	SLK581	DOB	SEX	DOB ACCURACY	COUNTRY	INDIG STATUS	
# LANGUAGE	CLIENT	SOURCE	ENROLMENT	DISCHARGE	CESSATION	SETTING	USE	INJECTION	DRUG	ODC1	ODC2	ODC3	ODC4	ODC5	
# TREAT	OTT1	OTT2	OTT3	OTT4	OTT5	POSTCODE	LIVING	ACCOM	PREVIOUS TREATMENT	MENTAL HEALTH

#'ENROLLING PROVIDER': 'Tim Ireson' , 'ID':'11525','FULL NAME':'SILBY, JAYDEN','EID':'820002000','SLK581':'ILYAY111219961',
            #         'DOB':'3052010','SEX':'Male','AGE':'22',
            #         'Date accuracy indicator': 'AAA - Day, month and year are accurate', 'Country of birth': 'Australia',
            #         'Indigenous status': 'Neither Aboriginal nor Torres Strait Islander origin',
            #         'Preferred language': 'English', 'Client type': 'Own alcohol or other drug use', 'Source of referral':'Self', 'Commencement date': '4022019',
            #         'End date': '', 'DAYS ENROLLED': '', 'Reason for cessation': '', 'Treatment delivery setting': 'Non-residential treatment facility',
            #         'Method of use for PDC': 'Sniffs (powder)', 'Injecting drug use status': 'Never injected', 'Principle drug of concern': 'Diazepam',
            #         'ODC1': '', 'ODC2': '', 'ODC3': '', 'ODC4': '', 'ODC5': '', 'Main treatment type': 'Counselling', 'OTT1': '', 'OTT2': '', 'OTT3': '',
            #         'OTT4': '', 'OTT5': '', 'Postcode (Australian)': '2906', 'Living arrangements': 'Alone', 'Usual accommodation': 'Private residence',
            #         'Previous alcohol and other drug treatment received': 'No previous treatment received', 'Mental health': 'Never been diagnosed', 'DIAGNOSIS': '', 'ARCADIA': '',
            #         'TREATED IN': '', 'PROGRAM': 'Counselling and Case Management', 'Surname': 'SILBY', 'First name': 'JAYDEN'}