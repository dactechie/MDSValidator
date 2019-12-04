
drug_usage = {

'Alcohols nfd'    : 	['Ingests'],
'Alcohol'         :   ['Ingests',	'Injects',	'Not stated/inadequately described', 'Smokes',	'Sniffs (powder)'],
'Amphetamines, n.e.c.'     : 	['Ingests',	'Inhales (vapour)',	'Injects',	'Smokes'],
'ANALGESICS'      : ['Ingests'],
'Amphetamine'     : 	['Ingests',	'Inhales (vapour)',	'Injects',	'Smokes'],

'Benzodiazepines nfd': ['Ingests'],
'Benzodiazepines, n.e.c.': ['Ingests', 'Injects',	'Smokes', 'Sniffs (powder)' ],
'Buprenorphine'   : 	['Ingests'],

'Caffeine'        : ['Ingests'],

'Cannabinoids'    : 	['Ingests',	'Inhales (vapour)',	'Smokes'],
'Cocaine' : 	['Ingests','Sniffs (powder)', 'Injects'],
'Codeine'         : 	['Ingests'],

'Dexamphetamine'  : 	['Injects'],
'Diazepam'        : 	['Ingests'],

'GHB type Drugs and Analogues, n.e.c.': ['Ingests', 'Inhales (vapour)'],
'Heroin' : 	['Ingests',	'Injects', 'Smokes', 'Inhales (vapour)', 'Not stated/inadequately described'],
'Ketamine'        : 	['Ingests', 'Sniffs (powder)'],

'Methamphetamine' : 	['Ingests',	'Inhales (vapour)',	'Injects',	'Not stated/inadequately described', 'Smokes',	'Sniffs (powder)'],
'Methadone'       : 	['Injects', 'Ingests', 'Smokes', 'Not stated/inadequately described'],
'MDMA'            : 	['Ingests','Sniffs (powder)'],
'MDA'             : 	['Ingests'],
'Morphine': ['Ingests', 'Injects', 'Smokes','Not stated/inadequately described','Inhales (vapour)'],

'Nicotine': ['Ingests',	'Inhales (vapour)', 'Smokes'],
'Not Stated / Inadequately Described' : 	['Injects', 'Ingests',	'Not stated/inadequately described'],
'Not stated/inadequately described' : ['Not stated/inadequately described'],            # TODO cleanup with the above

'Opioid analgesics nfd' : ['Ingests'],
'Other Antidepressants and Antipsychotics, n.e.c.': ['Ingests'],


'Other Drugs of Concern' : 	['Not stated/inadequately described', 'Sniffs (powder)'],
'Oxycodone'       : 	['Ingests'],

'Tramadol'        : 	['Ingests'],
'Zolpidem': 	['Ingests']
}


drug_usage['Cannabinoid agonists'] = drug_usage['Cannabinoids']
drug_usage['Cannabinoids and Related Drugs, n.e.c.'] = drug_usage['Cannabinoids']
