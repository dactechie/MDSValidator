from MDS_constants import MDS as M

rule_definitions = [
  {
    "message": f"If {M['METHOD']} is 'Injects', '{M['INJ_USE']}' can't be 'Never injected'.",
    "field": M['INJ_USE'],
    "type" :"Error",
    "rule": {"if": [ # Rule #4
              {"==": [{"var": M['INJ_USE']}, "Never injected" ]},
              {"!==": [{"var":M['METHOD']}, "Injects" ]},
              True
            ]}
  },
  {
    "message": M['METHOD'] + " must make sense with PDC.",
    "field": M['METHOD'],
    "type" :"Error",
    "rule": {"if": [ # Rule #3
              {"==": [{"var":M['PDC']}, "Alcohol" ]}, {"==": [{"var":M['METHOD']}, "Ingests"]},
              {"==": [{"var":M['PDC']}, "Cannabis" ]}, {"==": [{"var":M['METHOD']}, "Smokes"]},
              True
            ]}
  },
  {
      "message": "Can't have duplicate PDC/ODCs.",
      "field": M['PDC'],
      "type" :"Error",
      "rule":{"!": 
          {"has_duplicate_values":[{"var":M['PDC']},{"var":"ODC1"},{"var":"ODC2"},{"var":"ODC3"},{"var":"ODC4"},{"var":"ODC5"}]}
      }
  },
  {
      "message": "Can't have duplicate MTT/OTTs.",
      "field": M['MTT'],
      "type" :"Error",
      "rule":{"!": 
          {"has_duplicate_values":[{"var":M['MTT']},{"var":"OTT1"},{"var":"OTT2"},{"var":"OTT3"},{"var":"OTT4"},{"var":"OTT5"}]}
      }
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Other's AOD use', '{M['PDC']}' and '{M['METHOD']}' must be empty.",
    "field": M['CLNT_TYP'],
    "type" :"Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Other's alcohol or other drug use" ]},
              {"and": [
                  {"==": [{"var":M['PDC']}, "" ]}, {"==": [{"var":"ODC1"}, ""]},
                  {"==": [{"var":M['METHOD']}, "" ]}
              ]},
              True
            ]}
  },
  {
    "message": f"When {M['CLNT_TYP']} is 'Own AOD use', '{M['PDC']}' and '{M['METHOD']}' must NOT be empty.",
    "field": M['CLNT_TYP'],
    "type" :"Error",
    "rule": {"if": [  # rule 9
              {"==": [{"var":M['CLNT_TYP']}, "Own alcohol or other drug use"]},
              {"and": [
                  {"!==": [{"var":M['PDC']}, "" ]},
                  {"!==": [{"var":M['METHOD']}, ""]},
              ]},
              True
            ]}
  },
  {
      "message": "Check SLK",
      "field": M['SLK'],
      "involvedFields":[ M['DOB']], # TODO : not showing 'imva;od SLK for 33333 because dateformat is wrong.
      "type" :"Error",
      "rule":
          {"check_slk":[{"var":M['ID']}, {"var":M['SLK']}, {"var":M['FNAME']},
                        {"var":M["LNAME"]},{"var":M["DOB"]},{"var":M["SEX"]}
                       ]
          }
  },
  {
    "message": f"For Main Treatment Type: 'Assessment' or 'Info/Education only', the episode duration must be less than 90 days.",
    "field": M['END_DATE'],
    "involvedFields":[ M['END_DATE'], M['COMM_DATE']],
    "type" :"Warning",
    "rule":{
      "if": [  # rule 12 & 13
            {"and": [
              {"!=": [{"var":M['END_DATE']}, ""] } ,
              {"in": [{"var":M['MTT']}, ["Assessment only","Information and education only"]]}
            ]},
        {"<":[
              {"-":[{"var":'O'+M["END_DATE"]},{"var":'O'+M["COMM_DATE"]}]},
              90
            ]
        }
        ,True
      ]}
  },
  {
    "message": f"{M['DOB']} must be < {M['COMM_DATE']}",
    "field": M['DOB'],
    "involvedFields":[ M['DOB'], M['COMM_DATE']],
    "type" :"Error",
    "rule" :{"<" : [{ "var" : 'O'+M['DOB'] }, { "var" : 'O'+M['COMM_DATE']}]},
  },
  {
    "message": f"{M['COMM_DATE']} must be <= {M['END_DATE']}",
    "field": M['COMM_DATE'],
    "involvedFields":[ M['END_DATE'], M['COMM_DATE']],
    "type" :"Error",
    "rule" : {"if": [  # rule 9
              {"!=": [{"var":M['END_DATE']}, ""] } ,
              {"<=" :  [{ "var" : 'O'+M['COMM_DATE'] }, { "var" : 'O'+M['END_DATE']} ]},
              True
            ]
    }
  }
]

