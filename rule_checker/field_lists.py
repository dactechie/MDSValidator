from ..AOD_MDS.logic_rules.common import rule_definitions

"""
TODO: if checking TSS data, include TSS rules
"""

rd_wo_involved_fields = (rd for rd in rule_definitions if 'involvedFields' not in rd)
rd_with_involved_fields = (rd for rd in rule_definitions if 'involvedFields' in rd)
involved_field_sets =  (set(rd['involvedFields']) for rd in rd_with_involved_fields)
