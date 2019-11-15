from ..constants import MDS as M
from ..constants import MDS_ST_FLD, MDS_END_FLD

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
  },

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

  {
    "message": f"If {M['METHOD']} is 'Injects', '{M['INJ_USE']}' can't be 'Never injected'.",
    "field": M['INJ_USE'],
    "type" : "Error",
    "rule": {"if": [ # Rule #4
              {"==": [{"var": M['INJ_USE']}, "Never injected"]},
              {"!==": [{"var": M['METHOD']}, "Injects"]},
              True
            ]}
  },
  {
    "message": f"{M['METHOD']}  must make sense with PDC.",
    "field":  M['METHOD'],
    "type" : "Error",
    "rule": {"if": [
        {"!=": [{"var":M['PDC']}, "" ]},
        {"is_valid_drug_use": [{"var":M['PDC']} , {"var":M['METHOD']} ]},
        True
    ]}
  },

  # Repeated drug of concern
  # Priority: Critical
  # ValidationCode: Logic 06
  # Records were found where the same drug code was repeated in Principal drug of concern or Other drug of concern (1-5). 
  # An episode may only have each drug code recorded once, unless that code is '9999' (miscellaneous drugs).
  {
    "message": "Can't have duplicate PDC/ODCs.",
    "field": 'ODC5',
    "type" : "Error",
    "rule": {"!": 
        {"has_duplicate_values": [{"var": 'ODC5'}, [{"var": 'ODC4'}, {"var": 'ODC3'},
                                  {"var": 'ODC3'}, {"var": 'ODC1'}, {"var": M['PDC']}]]}
    }
  },
  {
    "message": "Can't have duplicate PDC/ODCs.",
    "field": 'ODC4',
    "type" : "Error",
    "rule": {"!": 
        {"has_duplicate_values": [{"var":'ODC4'}, [{"var": 'ODC3'}, {"var": 'ODC2'},
                                  {"var": 'ODC1'}, {"var": M['PDC']}]]}
    }
  },
  {
    "message": "Can't have duplicate PDC/ODCs.",
    "field": 'ODC3',
    "type" : "Error",
    "rule": {"!": 
        {"has_duplicate_values": [{"var": 'ODC3'}, [{"var": 'ODC2'},
                                  {"var": 'ODC1'}, {"var": M['PDC']}]]}
    }
},
  {
    "message": "Can't have duplicate PDC/ODCs.",
    "field": 'ODC2',
    "type" :"Error",
    "rule":{"!": 
        {"has_duplicate_values": [{"var": 'ODC2'},[{"var": 'ODC1'},{"var": M['PDC']}]]}
    }
  },
  {
    "message": "Can't have duplicate PDC/ODCs.",
    "field": M['PDC'],
    "type" : "Error",
    "rule": {"!": 
        {"has_duplicate_values": [{"var": M['PDC']}, [{"var": 'ODC1'}]]}
    }
  },
  {
      "message": "Can't have duplicate MTT/OTTs.",
      "field": 'OTT4',
      "type" :"Error",
      "rule":{"!": 
          {"has_duplicate_values": [{"var": 'OTT4'}, [{"var": 'OTT1'}, {"var": 'OTT2'},
                                    {"var": 'OTT3'}, M['MTT']]]}
      }
  },
  {
      "message": "Can't have duplicate MTT/OTTs.",
      "field": 'OTT3',
      "type" :"Error",
      "rule":{"!": 
          {"has_duplicate_values": [{"var": 'OTT3'}, [{"var": 'OTT1'}, {"var": 'OTT2'}, M['MTT']]]}
      }
  },
  {
      "message": "Can't have duplicate MTT/OTTs.",
      "field": 'OTT2',
      "type" :"Error",
      "rule":{"!": 
          {"has_duplicate_values": [{"var": 'OTT2'}, [{"var": "OTT1"}, M['MTT']]]}
      }
  },
  {
      "message": "Can't have duplicate MTT/OTTs.",
      "field": M['MTT'],
      "type" : "Error",
      "rule":{"!": 
          {"has_duplicate_values": [{"var":M['MTT']}, [{"var":"OTT1"}]]}
      }
  },
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

  # Missing drugs of concern
  # Priority: Critical
  # Logic 08
  # Records were found with missing drug of concern records. If other drugs of concern 2-5 are supplied, then a value must be
  # supplied for other drug of concern 1 and for all previous other drugs of concern. 
  # For example, if other drug of concern 3 is supplied, other drugs of concern 1 and 2 must also be supplied.
  {
    "message": f"ODCs of higher number can't be present when a lower number ODC is absent.",
    "field": 'ODC1',
    "type" : "Error",
    "rule":{"!": 
            {"has_blanks_in_otherdrugs": [{"var": M['PDC']}, {"var": "ODC1"}, {"var": 'ODC2'},
                                          {"var": "ODC3"}, {"var": 'ODC4'}, {"var": "ODC5"}
            ]}
        }
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

  # Date of cessation out of collection period
  # Priority: Critical
  # Rule 10
  # Records were found where Date of cessation did not fall within the collection period. 
  # Records where Date of cessation falls outside the period from July 1, 2018 to June 30, 2019 are not in the scope of the collection.
  # Please review and amend the Date of cessation or exclude the episodes.

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

  # Potential duplicate records
  # ValidationCode : Duplicate Eps
  # Priority: Critical
  # Records have been identified as possible duplicates (two records have been presented with the same data for Establishment ID, 
  # Person ID, Client type, Date of commencement of treatment, Date of cessation of treatment, State, Sex, Principal drug of concern,
  #  Main treatment type and Treatment delivery setting). Please confirm if these are valid records.
  
  # Checked in  AOD_MDS\helpers.py for prep_and_check_overlap
  #


  # Incorrect additional treatment type
  # ValidationCode: Logic 10
  # Records were found where Main treatment type was '5' (Support and case management only), '6' (Information and education only) or 
  # '7' (Assessment only) and an additional treatment was recorded. 
  # Records where that Main treatment type specifies that it is the 'only' treatment cannot have additional treatment types.

  {
    "message": "Incorrect additional treatment type (when MTT has the word 'only')",
    "field": M['MTT'],
    "type" : "Error",
    "rule": {"!":
        {"if": [
            {"==" : ["only", 
                          {"substr": [ {"var": M['MTT'] },-4] }
                    ] },
            {"!=":  [ {"cat": [
                        {"var":'OTT1'}, {"var":'OTT2'}, {"var":'OTT3'}, {"var":'OTT4'},{"var":'OTT5'} 
                        ]},
                    "" ]}
          ]
        }
      }
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
]

