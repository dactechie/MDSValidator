from AOD_MDS.constants import MDS as M

rule_definitions = [
  {
    "message": f"Arcadia-Resi program only does the following treatment types: Counselling, Support and case management, Rehab, Detox",
    "field": M['MTT'],
    "type" : "Error",
    "rule": {"!": 
              {"or" : [
                  {"==": [{"var": M['MTT']}, "Information and education"]},
                  {"==": [{"var": M['MTT']}, "Pharmacotherapy"]}                  
              ]}
            }
  },
  {
    "message": f"If {M['USACC']} is 'Prison/remand centre/youth training centre', '{M['TRDLVSTG']}' has to be 'Outreach setting'.",
    "field": M['TRDLVSTG'],
    "type" : "Error",
    "rule": {"if": [ 
              {"==": [{"var": M['USACC']}, "Prison/remand centre/youth training centre"]},
              {"==": [{"var": M['TRDLVSTG']}, "Outreach setting"]},
              True
            ]}
  },
  {
    "message": f"Arcadia-Resi program does not provide service (treatment delivery) in Home/'Other' settings.",
    "field": M['TRDLVSTG'],
    "type" : "Error",
    "rule": {"!": 
              {"or" : [
                  {"==": [{"var": M['TRDLVSTG']}, "Home"]},
                  {"==": [{"var": M['TRDLVSTG']}, "Other"]}
              ]}
            }
  },
  {
    "message": f"If {M['TRDLVSTG']} is Residential treatment', '{M['MTT']}' has to be Withdrawal Mgmt.(Detox) / Rehab.",
    "field": M['TRDLVSTG'],
    "type" : "Error",
    "rule": {"if": [ 
              {"==": [{"var": M['TRDLVSTG']}, "Residential treatment facility"]},
              {"in": [{"var":M['MTT']}, ["Rehabilitation","Withdrawal management (detoxification)"]]},
              True
            ]}
  },
]
