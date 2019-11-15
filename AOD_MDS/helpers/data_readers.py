
import copy
import csv
from MDSValidator.logger import logger
from MDSValidator.AOD_MDS.constants import MDS
from MDSValidator.utils import remove_unicode


def read_header(filename: str) -> list:
    with open(filename, 'r') as csvfile:
        headers = [header for header in csvfile.readline().split(',')]
        headers[-1] = headers[-1].strip('\n')
        return headers



def _split_fullname(reader) -> list:
  data_dicts = []
  for i, r in enumerate(reader):
    if  "".join(r.values()) == '':
        logger.error(f"\n\tFound Blank row at {i}. Quitting...")
        return None
    row = copy.deepcopy(r)
    if row.get("FULL NAME"):              
        row[MDS['LNAME']], row[MDS['FNAME']]  = str.split(row["FULL NAME"], ", ")
        del row["FULL NAME"]
    
    data_dicts.append(row)

  return data_dicts


# TODO clean this up (use a generator)
def read_data(filename: str, data_header: dict, hmap: dict, 
                             start_end: dict, all_eps=True) -> dict:
    """
    - Assumes that if a "FULL NAME" column exists, all rows will have a format of
        'LastName, FirstName'.
    - Sometimes the header may have unicode (special) characters, cleans before use.
    - hmap is a map of the header fields with official MDS translations,
        where cleansing was required.
    - all_eps == False => Closed eps only
    """
    #data_header = fix_headers(data_header)
    with open(filename, 'r') as csvfile:
        csvfile.readline()
        reader = csv.DictReader(csvfile, data_header)
        
        if MDS['FNAME'] not in data_header and "FULL NAME" in data_header:
          rows = _split_fullname(reader)           
          reader = rows
          data_header.remove("FULL NAME")
          data_header.extend([MDS['FNAME'], MDS['LNAME']])
        
        clean_headers = {dh: remove_unicode(dh) for dh in data_header}
        # [ch for ch in clean_headers.values() if ch in data_header] == data_header
        # True
        tmp_k = None
        result = []
        ii = 0
        for i, row in enumerate(reader):
            if  "".join(row.values()) == '':
              logger.error(f"\n\tFound Blank row at {i}. skipping to next row...")
              continue

            if not all_eps and not row[MDS['END_DATE']]:
              continue

            result.append({})
            for k, v in row.items():
                tmp_k = clean_headers[k]
                # if tmp_k in hmap:
                #     result[i][hmap[tmp_k]] = v
                # else:
                result[ii][tmp_k] = v
            ii = ii + 1

        #result = [ {k:v for k, v in row.items()} for row in reader if hmap[k]]
 
        return { "episodes" :result }
