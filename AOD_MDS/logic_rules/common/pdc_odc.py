from ...constants import MDS as M

rule_definitions = [

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
  }

 ]