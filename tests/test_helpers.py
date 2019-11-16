import os
import pytest
from MDSValidator.AOD_MDS.helpers import getSLK, translate_to_MDS_header, translate_to_MDS_values
from MDSValidator.logger import logger


def test_getSLK():
    first_name ="Aftab"
    surname  = "Jalal"
    dob = "21/07/1981" 
    sex  = "Male"
    assert getSLK(first_name,surname,dob,sex) == "ALLFT210719811"


def test_translate_to_MDS_header():
    header = ["ID", "Method of use for principal drug of concern" ]
    converted_header, warnings = translate_to_MDS_header(header)
    logger.info(warnings)
    assert converted_header == ["ID", "Method of use for PDC"]


def test_translate_to_MDS_values():
    data = [ { 'ID': '101010',  'Client type': "Own drug use" }]
    warnings = translate_to_MDS_values(data)
    logger.info(warnings)

    assert data[0]['Client type'] == "Own alcohol or other drug use"
    
    assert warnings[0] == { "index": 0, "cid": '101010', 
                            "required": "Own alcohol or other drug use", 
                            "got": "Own drug use"}
