import os
import pytest
#from JSONValidator import JSONValidator
from helpers import getSLK, translate_to_MDS_header, translate_to_MDS_values

# @pytest.fixture(scope='session')
# def headers_map():
#     # alias_lower -> Officla MDS name
    
#     # k (official name) : v [] -> array of aliases or accepted values
#     return {
#         "Client ID" : "ID",
#         "PID" : "ID",
#         "Method of use for PDC" : "Method of use for principal drug of concern"
#     }
# def json_validator(request):
#     schema_dir = os.path.join(os.getcwd(), 'schema/')
#     schema_file_name = os.path.realpath(os.path.join(schema_dir, 'schema.json'))
#     return JSONValidator(schema_dir, schema_file_name)

    #request.


# def test_getSLK():
#     first_name ="Aftab"
#     surname  = "Jalal"
#     dob = "21/07/1981"
#     sex  = "Male"
#     assert getSLK(first_name,surname,dob,sex) == "ALLFT210719811"


# def test_translate_to_MDS_header():
#     header = ["ID", "Method of use for principal drug of concern" ]
#     converted_header, warnings = translate_to_MDS_header(header)
#     print(warnings)
#     assert converted_header == ["ID", "Method of use for PDC"]


def test_translate_to_MDS_values():
    data = [ { 'ID': '101010',  'Client type': "Own drug use" }]
    warnings = translate_to_MDS_values(data)
    
    assert data[0]['Client type'] == "Own alcohol or other drug use"
    
    assert warnings[0] == { "index": 0, "cid": '101010', 
                            "required": "Own alcohol or other drug use", 
                            "got": "Own drug use"}
