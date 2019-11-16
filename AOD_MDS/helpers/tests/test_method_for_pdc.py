

import pytest
from AOD_MDS.helpers.others import is_valid_drug_use


@pytest.mark.parametrize("drug, method ,expected", [
    ("Cocaine", "Ingests", True),  
    ("Nicotine", "Injects", False),
    ("Nisdfsdcotine", "Injects", False),
    ("Cocaine", "Indsfjects", False),
])
def test_usage_method(drug, method, expected):
  assert is_valid_drug_use(drug, method) == expected
