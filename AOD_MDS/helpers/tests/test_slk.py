
import pytest
from AOD_MDS.helpers import getSLK


@pytest.mark.parametrize("first_name, surname, dob, sex, expected", 
                          [
                            # plain n simple + invalid date (ignored)
                            ("Aftab", "Jalal", "30/02/1990", "Male", "ALLFT300219901"),
                            # special character 
                            ("Steve", "Far'ugia", "21/07/1981", "Female", "ARGTE210719812"),
                            # short last name + invalid date (ignored)
                            ("Ram", "Naik", "13/32/1990", "Not Stated", "AI2AM133219909")
                          ])
def test_getSLK(first_name,surname,dob,sex, expected):
    assert getSLK(first_name,surname,dob,sex) == expected
