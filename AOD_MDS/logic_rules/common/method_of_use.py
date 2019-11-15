from ...constants import MDS as M


rule_definitions = [
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
]