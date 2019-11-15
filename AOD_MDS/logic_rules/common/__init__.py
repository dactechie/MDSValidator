from .client_type import rule_definitions as ct_rules
from .dates import rule_definitions as dt_rules
from .method_of_use import rule_definitions as meth_rules
from .mtt_ott import rule_definitions as mtt_rules
from .pdc_odc import rule_definitions as pdc_rules
from .referral_source import rule_definitions as refsrc_rules
from .slk import rule_definitions as slk_rules
from .usualacc_treatdelvry import rule_definitions as ustre_rules

rule_definitions = [*ct_rules, *dt_rules, *meth_rules, *mtt_rules, *pdc_rules, *refsrc_rules, *slk_rules, *ustre_rules]
