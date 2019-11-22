
import pytest
#from AOD_MDS.helpers import  translate_to_MDS_header, translate_to_MDS_values
from AOD_MDS.constants import MDS as M
from AOD_MDS.helpers.translators import (fields_map, headers_map, 
            translate_to_MDS_header, translate_to_MDS_values)
from logger import logger



# pytest  tests/test_helpers.py::test_translate_to_MDS_header -vv
@pytest.mark.parametrize("header, expected", 
                          [(["PID", "Method of use for principal drug of concern" ],["ID", "Method of use for PDC"])]
                        )
def test_translate_to_MDS_header(header, expected):    
    converted_header, warnings = translate_to_MDS_header(header)
    logger.info(warnings)
    assert converted_header == expected


@pytest.mark.parametrize("data, expected, expected_warnings", 
                          [( # testing the field_values map as well..
                            [{ 'ID': '101010',  'Client type': "Own drug use" }], 
                            {'Client type':"Own alcohol or other drug use", 'ID': '101010'}, 
                            { "index": 0, "cid": '101010', "required": "Own alcohol or other drug use", "got": "Own drug use"}
                          ),
                          ( [{ 'ID': '12354',  'Client type': "Other's drug use" }], 
                            {'Client type':"Other's alcohol or other drug use", 'ID': '12354'}, 
                            { "index": 0, "cid": '12354', "required": fields_map[M['CLNT_TYP']]["Other's drug use"],
                              "got": "Other's drug use"}
                          )
                        ])
def test_translate_to_MDS_values(data, expected, expected_warnings):
    warnings = translate_to_MDS_values(data)
    logger.info(warnings)

    assert data[0] == expected
    
    assert warnings[0] == expected_warnings
