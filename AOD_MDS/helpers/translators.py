
import copy
from AOD_MDS.constants import MDS, MDS_Dates
from utils import v_warn_lam
from AOD_MDS.aliases import mds_aliases

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
alias_map_lam = lambda dict_of_alias_mappings : { alias: official_name
                                    for official_name, aliases in dict_of_alias_mappings.items()
                                    for alias in aliases }

alias_map_lam2 = lambda mds_dict_of_aliasedicts : { mds_field_name: alias_map_lam(alias_dict)
                                    for mds_field_name, alias_dict in mds_dict_of_aliasedicts.items()                                                                        
                                    }                                    

headers_map = alias_map_lam(mds_aliases['headers'])
fields_map = alias_map_lam2(mds_aliases['fields'])
val_translation_excluded_fields = ["ENROLLING PROVIDER", "EID", "Age", MDS["FNAME"], MDS["LNAME"],
                                   MDS["ID"], MDS["PCODE"], MDS["SLK"] ] + [MDS[md] for md in MDS_Dates]


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
    falias = {key: alias_dict for key, alias_dict in fields_map.items() if  key in fields_to_check}

    for i, ddict in enumerate(data):# each row                          [ {row1}, {row2}  {ID: 2}]
        #for data_key, v in ddict.items(): # each field within a row     row1->  { k1:v1 , k2:v2} 
        for data_key in fields_to_check:
            v =  ddict[data_key]
            conv_data_val = v.strip()
            if data_key in falias and conv_data_val in falias[data_key]:
                conv_data_val = falias[data_key][conv_data_val]
                warnings.append (
                        v_warn_lam(i,ddict[MDS['ID']],conv_data_val,v)
                    )
            data[i][data_key] = conv_data_val

    return warnings
