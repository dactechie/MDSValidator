
from ...constants import MDS as M

rule_definitions = [

  # Type 2 client with 'diversion - police or court' Source of referral
  # ValidationCode: Logic 33
  # Priority: Critical
  # Records were found where Client type was recorded as '2' (receiving treatment in relation to another person's drug use) and Source of referral is 
  # '9' (police diversion) or '10' (court diversion).  This combination of responses may not be valid or may require further explanation. 
  # Please review these records and amend any incorrect data.
  {
    "message": f"If {M['CLNT_TYP']} is 'Other's AOD use', '{M['SRC_REF']}' cannot be Police/Court diversion.",
    "field": M['SRC_REF'],
    "type" : "Error",
    "rule": {"if": [ 
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"and": [
                      {"!=": [{"var": M['SRC_REF']}, "Police diversion"]},
                      {"!=": [{"var": M['SRC_REF']}, "Court diversion"]}
                    ]
              },
              True
            ]}
  },

  # Inadequately described Principal drug of concern
  # ValidationCode: Logic 09
  # Priority: Critical
  # Records were found where Principal drug of concern was '0000' (inadequately described) or '0001' (not stated). 
  # Principal drug must have value other than 0000 or 0001 except where Source of referral is '9' (police diversion), 
  # '10' (court diversion), '98' (Other), or '99' (not stated). Please review and amend.
  {
    "message": "Inadequately described Principal drug of concern",
    "field": M['PDC'],
    "type" : "Error",
    "rule": {"if":[
              {"or" : [ {"==":  ["Inadequately Described",{"var": M['PDC']} ]},
                      {"==":  ["Not stated/inadequately described",{"var": M['PDC']} ]}
              ]},
              {"!=" : [" diversion", 
                          {"substr": [ {"var": M['SRC_REF'] },-10] }
               ] }
            ,
            True
      ]}
   },
]