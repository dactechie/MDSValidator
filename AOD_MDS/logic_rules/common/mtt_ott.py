from ...constants import MDS as M

rule_definitions = [

  # Incorrect additional treatment type
  # ValidationCode: Logic 10
  # Records were found where Main treatment type was '5' (Support and case management only), '6' (Information and education only) or 
  # '7' (Assessment only) and an additional treatment was recorded. 
  # Records where that Main treatment type specifies that it is the 'only' treatment cannot have additional treatment types.
  # {   # old rule  1 July 2018 onwards no "only"
  #   "message": "Incorrect additional treatment type (when MTT has the word 'only')",
  #   "field": M['MTT'],
  #   "type" : "Error",
  #   "rule": {"!":
  #       {"if": [
  #           {"==" : ["only", 
  #                         {"substr": [ {"var": M['MTT'] },-4] }
  #                   ] },
  #           {"!=":  [ {"cat": [
  #                       {"var":'OTT1'}, {"var":'OTT2'}, {"var":'OTT3'}, {"var":'OTT4'},{"var":'OTT5'} 
  #                       ]},
  #                   "" ]}
  #         ]
  #       }
  #     }
  # },

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
]