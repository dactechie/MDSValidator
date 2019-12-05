from ...constants import MDS as M
from ...constants import MDS_ST_FLD, MDS_END_FLD

rule_definitions = [

  # Long information and education only episode
  # Logic 15
  # Priority: Warning
  # Records were found where Main treatment type was '6' (Information education only) and episode duration was greater than 100 days. 
  # Please review these records and amend any incorrect data.
  {
    "message": f"For Main Treatment Type: 'Assessment' or 'Info/Education only', the episode duration must be less than 90 days.",
    "field": M['END_DATE'],
    "involvedFields": [M['END_DATE'], M['COMM_DATE']],
    "type" : "Warning",
    "rule": {
      "if": [  # rule 12 & 13
              {"and": [
                {"!=": [{"var":M['END_DATE']}, ""] } ,
                {"in": [{"var":M['MTT']}, ["Assessment only","Information and education only"]]}
              ]},
              {"<":[
                    {"-": [{"var":MDS_END_FLD},{"var":MDS_ST_FLD}]},
                    90
                  ]
              }
              ,True
            ]
        }
  },
  {
    "message": f"{M['DOB']} must be < {M['COMM_DATE']}",
    "field": M['DOB'],
    "involvedFields": [M['DOB'], M['COMM_DATE']],
    "type" : "Error",
    "rule" : {"<" : [{"var": 'O'+M['DOB'] }, {"var": MDS_ST_FLD}]},
  },
  {
    "message": f"{M['COMM_DATE']} must be <= {M['END_DATE']}",
    "field": M['COMM_DATE'],
    "involvedFields": [M['END_DATE'], M['COMM_DATE']],
    "type" :"Error",
    "rule" : {"if": [  # rule 9
              {"!=": [{"var": M['END_DATE']}, ""]},
              {"<=": [{"var": MDS_ST_FLD }, {"var": MDS_END_FLD} ]},
              True
            ]}
  },
  # Date of cessation out of collection period
  # Priority: Critical
  # Rule 10
  # Records were found where Date of cessation did not fall within the collection period. 
  # Records where Date of cessation falls outside the period from July 1, 2018 to June 30, 2019 are not in the scope of the collection.
  # Please review and amend the Date of cessation or exclude the episodes.

  {
    "message": f"Episode End Date is not in the reporting period",
    "field": M['END_DATE'],
    "involvedFields": [M['END_DATE']],
    "type" :"Error",
    "rule" : {"!": {"and":[
                  {"!=": [{"var": M['END_DATE']}, ""]},
                  {"is_notin_period": [ {"var": MDS_END_FLD} ]}
                ]
            }}
  },
  # Potential duplicate records
  # ValidationCode : Duplicate Eps
  # Priority: Critical
  # Records have been identified as possible duplicates (two records have been presented with the same data for Establishment ID, 
  # Person ID, Client type, Date of commencement of treatment, Date of cessation of treatment, State, Sex, Principal drug of concern,
  #  Main treatment type and Treatment delivery setting). Please confirm if these are valid records.
  
  # Already Checked in  AOD_MDS\helpers.py for prep_and_check_overlap
  #

]

# TODO
  # Client is over 100
  # Priority: Critical
  # Logic 01
  # Records were found where a client's Date of birth indicated that they were over 100 years old. 
  # All Dates of birth must be within 100 years of the Date of commencement, unless using the default Date of birth (01011900).
  #
  
  # Client is under 10
  # Priority: Critical
  # Logic 02
  # Records were found where a client's Date of birth indicated they were under ten years old at the Date of commencement of the episode. 
  # Please check that Date of Birth is correct as clients under ten are not in the scope of the AODTS NMDS.
  # Please amend Date of birth or exclude records.

  # Invalid Date of birth
  # Priority: Critical
  # Rule 02
  # Records were found where Date of birth was not a valid code. Please ensure that Date of birth is a valid date and is in the format DDMMYYYY. 
  # For example, a client born of November 3rd, 1986 should have the following Date of birth entry: 03111986. 
  # Date of birth should not contain any slashes, dashes or other nonnumeric characters.

