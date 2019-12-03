from ..constants import MDS as M
from ..constants import MDS_ST_FLD, MDS_END_FLD

rule_definitions = [
  {
    "message": f"Althea only does the following treatment types: Pharmacotherapy, Counselling, Support and case management and Information and education",
    "field": M['MTT'],
    "type" : "Error",
    "rule": {"!": 
              {"or" : [
                  {"==": [{"var": M['MTT']}, "Rehabilitation"]},
                  {"==": [{"var": M['MTT']}, "Withdrawal management (detoxification)"]}
              ]}
            }
  },
  {
    "message": f"Althea team does not provide service (treatment delivery) in Home/'Other'/Resi setting ",
    "field": M['TRDLVSTG'],
    "type" : "Error",
    "rule": {"!": 
              {"or" : [
                  {"==": [{"var": M['TRDLVSTG']}, "Home"]},
                  {"==": [{"var": M['TRDLVSTG']}, "Other"]},
                  {"==": [{"var": M['TRDLVSTG']}, "Residential treatment facility"]},
              ]}
            }
  },
    # Opioid Pharmacotherapy only
  # ValidationCode: Logic 20
  # Records were found where Main treatment type was coded 4 (pharmacotherapy) but Other treatment type 1 was blank.  
  # The scope of the AODTS NMDS excludes 'clients who are on an opioid pharmacotherapy program and who are not 
  # receiving any other form of treatment that falls within the scope of the AODTS-NMDS'. 
  # Please check that no addition treatment information is available. For more information, please contact the AIHW.
  {
    "message": f"If MTT is Pharmacotherapy, OTT1 should be present",
    "field": M['MTT'],
    "type" : "Error",
    "rule":  {"!" : {"and": [
                {"==": [{"var": M['MTT']}, "Pharmacotherapy"]},
                {"==": [{"var": 'OTT1'}, "" ]}                
            ]}}
  }
  
]