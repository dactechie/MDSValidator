from ...constants import MDS as M

rule_definitions = [

  {
    "message": f"If {M['USACC']} is 'Prison/remand centre/youth training centre', '{M['TRDLVSTG']}' has to be 'Outreach setting'.",
    "field": M['TRDLVSTG'],
    "type" : "Error",
    "rule": {"if": [ 
              {"==": [{"var": M['USACC']}, "Prison/remand centre/youth training centre"]},
              {"==": [{"var": M['TRDLVSTG']}, "Outreach setting"]},
              True
            ]}
  }

]

# TODO

  ############################################################ WARNING #######################################################################
  # Principal drug of concern is 9999 'other'
  # Logic 25
  # Warning
  # Records were found where Principal drug of concern was '9999' (Other). Please note that this code should only be used where
  #  the Principal drug of concern is not found elsewhere in the Australian Standard Classification of Drugs of Concern (ASCDC 2011, ABS cat.no.1248.0).
  #  Please check that more accurate information is not available and amend accordingly.

  # Inadequately described Principal drug of concern, acceptable source of referral
  # Logic 26
  # Warning
  # Records were found where Principal Drug of concern is '0000' (inadequately described) or '0001' (not stated) and Source of referral is '9' (police diversion),
  #  '10' (court diversion), '98' (other) or '99' (not stated). These records are valid and will be accepted if formally submitted. However, 
  # please check that no accurate Principal drug of concern information is available and amend accordingly.

  # Check date accuracy indicator
  # Logic 27
  # Warning
  # Records were found with less common date accuracy indicator codes. Where date of birth and date accuracy indicator are entered according to the collection specifications,
  #  these codes are expected: AAA (If a date of births accurate then the Date accuracy indicator should be AAA), UUE (If the age of the person is estimated, 
  # then the Date accuracy indicator should be UUE. Day and month are 'unknown' and the year is 'estimated') or UUU (No information is known about the person's 
  # date of birth or age). Please check the date  of birth and date accuracy indicator of these records.


