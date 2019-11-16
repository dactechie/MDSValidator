
from datetime import datetime
import pytest
from AOD_MDS.helpers.overlap import check_overlap
from AOD_MDS.constants import MDS as M

current_ep = {'ID' : '1234',
       'idx' : '41',M['COMM_DATE'] : datetime(2018,9,1).toordinal(), M['END_DATE'] : datetime(2019,10,15).toordinal()}

client_eps = [
     {'idx': '0', M['COMM_DATE']: datetime(2019,10,1).toordinal(), M['END_DATE']: datetime(2019,11,1).toordinal() },
     {'idx': '1', M['COMM_DATE']: datetime(2019,12,1).toordinal(), M['END_DATE']: datetime(2019,12,15).toordinal()},
     current_ep
]


errors = {'0':[], '41':[] }

expected = {'0': [{'cid': '1234',
              'etype': 'logic', 'field': 'End date', 'index': '0',
              'message': 'Overlaps with other episode Start: 737333 End: 737364'}],
       '41': [{'cid': '1234', 'etype': 'logic', 'field': 'End date',
              'index': '41','message': 'Overlaps with other episode '
              'Start: 01/10/2019 End: 01/11/2019'}]}


@pytest.mark.parametrize("current_ep, client_eps, errors, rec_idx, expected", [
              (current_ep, client_eps, errors, '41', expected)
          ])
def test_overlap(current_ep, client_eps, errors, rec_idx, expected):
  check_overlap(current_ep, client_eps, errors, rec_idx)
  assert errors == expected


