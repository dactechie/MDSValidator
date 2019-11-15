from ...constants import MDS as M

rule_definitions = [
  {
      "message": "Check SLK",
      "field": M['SLK'],
      "involvedFields": [M['DOB']], # TODO : not showing 'imva;od SLK for 33333 because dateformat is wrong.
      "type" : "Error",
      "rule":
          {"check_slk": [{"var":M['ID']}, {"var":M['SLK']}, {"var":M['FNAME']},
                         {"var":M["LNAME"]},{"var":M["DOB"]},{"var":M["SEX"]}
                        ]
          }
  },
]

# All of the below are checked inside the code in check_slk function.

  # Invalid Letters of family name or Letters of given name
  # Priority: Critical
  # Rule 27
  # Records were found where the Letters of family name or Letters of given name contained non standard characters.
  # Please check that the first 5 characters in the Statistical linkage key are either letters of the alphabet or the numbers '9' or '2'.

  # SLK 581 is the wrong length
  # ValidationCode: Rule 28
  # Priority
  # Records were found where Statistical linkage key was either too long or too short or contains spaces. 
  # Please check that Statistical linkage key 581 is 14 characters long, with NO spaces and contains letters of 
  # family name (3 letters) Letters of given name (2 letters) date of birth (8 numbers) and sex(1 number). 
  
  # SLK 581 Date of birth component does not match actual Date of birth variable
  # Rule 29
  # Priority:
  # Records were found where the Statistical linkage key, Date of birth component does not match the Date of birth variable. 
  # Please ensure the SLK date of birth component is the same value as the Date of birth variable.

  # SLK 581 Sex component does not match Sex variable
  # ValidationCode: Rule 30
  # Priority: 
  # Records were found where the Statistical linkage key, Sex component does not match the Sex variable. 
  # Please ensure the SLK, Sex component is the same value as the Sex variable.
  
  # Problem with use of '2' in Letters of family name
  # Logic 17
  # Priority: Critical
  # Records were found where '2' were used incorrectly in the Letters of family name component of the Statistical linkage key 581. 
  # '2' should only be used to fill in space when the family name is too short.
