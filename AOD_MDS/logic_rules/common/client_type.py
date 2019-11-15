from ...constants import MDS as M

rule_definitions =[
 # Type 2 client with drug related items
  # Priority: Critical
  # ValidationCode Logic 04
  # Records were found a where a Client type was recorded as '2' (receiving treatment in relation to another person's drug use). 
  # However values exist for Injecting drug use, Principal drug of concern, Other drug of concern (1-5) or Method of use 
  {
    "message": f"When {M['CLNT_TYP']} is 'Other's AOD use', '{M['PDC']}' must be empty.",
    "field": M['PDC'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"==": [{"var":M['PDC']}, "" ]},
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Other's AOD use', '{M['METHOD']}' must be empty.",
    "field": M['METHOD'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"==": [{"var":M['METHOD']}, "" ]},
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Other's AOD use', '{M['INJ_USE']}' must be empty.",
    "field": M['INJ_USE'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"==": [{"var":M['INJ_USE']}, "" ]},
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Other's AOD use', all ODCs must be empty.",
    "field": 'ODC1',
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"and": [
                  {"==": [{"var":"ODC1"}, ""]},
                  {"==": [{"var":"ODC2"}, ""]}, {"==": [{"var":"ODC3"}, ""]},
                  {"==": [{"var":"ODC4"}, ""]}, {"==": [{"var":"ODC5"}, ""]}
              ]},
              True
            ]}
  },

  {
    "message": f"When {M['CLNT_TYP']} is 'Own AOD use', '{M['PDC']}' must NOT be empty.",
    "field": M['PDC'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Own alcohol or other drug use"]},
              {"!==": [{"var":M['PDC']}, "" ]},              
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Own AOD use', '{M['METHOD']}' must NOT be empty.",
    "field": M['METHOD'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Own alcohol or other drug use"]},
              {"!==": [{"var":M['METHOD']}, "" ]},              
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Own AOD use', '{M['INJ_USE']}' must NOT be empty.",
    "field": M['INJ_USE'],
    "type" : "Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Own alcohol or other drug use"]},
              {"!==": [{"var":M['INJ_USE']}, "" ]},              
              True
            ]}
  },

]