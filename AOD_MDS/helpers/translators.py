
import copy
from MDSValidator.AOD_MDS.constants import MDS
#                                       rd_wo_involved_fields)
from MDSValidator.utils import v_warn_lam
from MDSValidator.AOD_MDS.aliases import mds_aliases

'''
Input data file may not have the exact spelling/case as the official MDS fields
list_of_alias_mappings:
    [ { 'DOB' : ['Date of birth', 'DoB'] },
      { 'Principle drug of concern': ['PDC'] }
    ]
We prepare the Alias lookup table here. Result :
    {'Date of birth' : 'DOB',
        'DoB' : 'DOB',
        'PDC' : 'Principle drug of concern'
    }
'''
alias_map_lam = lambda list_of_alias_mappings : { alias: official_name
                                    for official_name, aliases in list_of_alias_mappings.items()
                                    for alias in aliases }

headers_map = alias_map_lam(mds_aliases['headers'])
fvalues_map = alias_map_lam(mds_aliases['fieldValues'])
val_translation_excluded_fields = ["ENROLLING PROVIDER", "EID", 
                                   MDS["ID"], MDS["DOB"], MDS["PCODE"], MDS["SLK"] ]



def translate_to_MDS_header(header):
    warnings = {}
    converted_header = copy.deepcopy(header)# [cleanse_string(h) for h in header]

    for i, h in enumerate(header):
        hlow = h#.lower()
        if hlow in headers_map:    # {alias1 : official_k1}, {alias2 : official_k1}, ...
            converted_header[i] = headers_map[hlow] #save the official MDS value in the new header
            warnings[h] = headers_map[hlow]
            #warnings[f"Header uses key:{h} instead of {headers_map[hlow]}"] = 1

    return converted_header, warnings
 

#without the deep copy
def translate_to_MDS_values(data):
    warnings = []
    fields_to_check = [k for k in data[0] if k not in val_translation_excluded_fields]

    for i, ddict in enumerate(data):# each row                          [ {row1}, {row2}  {ID: 2}]
        #for data_key, v in ddict.items(): # each field within a row     row1->  { k1:v1 , k2:v2} 
        for data_key in fields_to_check:
            v =  ddict[data_key]
            conv_data_val = v.strip()
            if conv_data_val in fvalues_map:
                conv_data_val = fvalues_map[conv_data_val]
                warnings.append (
                        v_warn_lam(i,ddict[MDS['ID']],conv_data_val,v)
                    )
            data[i][data_key] = conv_data_val

    return warnings
    