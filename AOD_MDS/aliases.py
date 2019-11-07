from .constants import MDS as M

mds_aliases = {
    # k (official name) : v [] -> array of aliases or accepted values
    "headers": {
        "ID": [ "PID", "Client ID"],
    },
    "fieldValues": {
        # REASON FOR CESSATION ##############
        "Ceased to participate without notice" : [
            "Ceased without notice"
        ],
        "Ceased to participate by mutual agreement": [
            "Ceased by mutual agreement"
        ],
        "Ceased to participate involuntary (non-compliance)": [
            "Ceased involuntary"
        ],
        "Transferred to another service provider" : [
            "Transferred to other provider"
        ],
        "Imprisoned, other than drug court sanctioned":["Imprisoned (not drug court)" ],

        # Mixed         
        "Other": ["Groups", "Other reason for cessation", "Shared Accommodation" ],
        
        "Non-residential treatment facility":[
            "Non-residential Facility"
        ],
        #Mental health
        "Diagnosed more than twelve months ago": [
            "Diagnosed more than 12 months ago"
        ],        
        "Not stated/inadequately described": [
            "Not stated / inadequately described",
            "Not Stated / Inadequately Described",
            "Not Stated",
            "Not known/inadequately described"
        ],

        # # PDC  - WARNING: the value is same as the above key
        # "Not Stated" : [
        #     "Not stated/inadequately described"
        # ],
        "Diagnosed three months ago or less" : [
            "Diagnosed 3 months ago or less"
        ],        
        "Never been diagnosed": [
            "Not Diagnosed, displaying possible symptoms"
        ],
        "Diagnosed more than three months ago but less than or equal to twelve months ago": [
            "Diagnosed between 3 months and 12 months ago",
            "Diagnosed more than three months ago or less than or equal to twelve month ago"
        ],

        "Last injected more than twelve months ago":[
            "Injecting drug use more than 12 months ago",
            "Injecting drug use more than twelve months ago (and not in last twelve months)"
        ],
        "Last injected three months ago or less": [
            "Current injecting drug use (last injectected prev 3 months)",
            "Current injecting drug use (last injected within the previous three months)"
        ],
        "Last injected more than three months ago but less than or equal to twelve months ago" : [ 
            "Injecting drug use between 3 to 12 months ago",
            "Injecting drug use more than three months ago but less than twelve months ago"
        ],

        "Own alcohol or other drug use": ["Own drug use" ],
        "Other's alcohol or other drug use": ["Other's drug use", "Other's alcohol/other drug use"],
        
        "Neither Aboriginal nor Torres Strait Islander origin": [
            "Neither Aboriginal nor TSI"
        ],
        "Aboriginal but not Torres Strait Islander origin": [
            "Aboriginal but not TSI"
        ],
        "Torres Strait Islander but not Aboriginal origin": [
            "TSI but not Aboriginal"
        ],
        "Both Aboriginal and Torres Strait Islander origin": [
            "Both Aboriginal and TSI"
        ],

        "Domestic-scale supported living facility" : ["Supported/Domestic-scale living facility"],
                
        "Counselling" : [ "DATS Counselling" ],
        "Support and case management only": [
            "Support & case management only"
        ],

        "Methamphetamine" : ["Crystal(meth) / Ice / Methamphetamine /Speed"],   # Coordinare Sep 2019 ; MJ's common Drugs translation
        "Lysergic acid diethylamide": ["LSD"],
        "Alcohol": [     "Ethanol"  , "Alcohol /Ethanol" ],
        "MDMA": [     "Ecstasy (MDMA)"   ],
        "Cannabinoids" : [   "Cannabis"    ],
        "Diazepam": ["diazepam"],
        
        "Nicotine" : [  "nicotine", "Nicotine/tobacco"  ],
        "Codeine": ["codeine"],
        "Amphetamines nfd" : [ "Amphetamines", "Amphetamines, nfd" ],
        "Benzodiazepines nfd" : ["Benzodiazepines"],
        "Analgesics nfd" : ["Other analgesics"],
        "Stimulants and Hallucinogens nfd" : [
            "Other stimulants/hallucinogens"
        ],
        "Sedatives and Hypnotics nfd": [
            "Other sedatives/hypnotics"
        ],
        "AAA - Day, month and year are accurate":[ "AAA" ],
        "EEE - Day, month and year are estimated":[ "EEE" ],
        "UUE - Day and month are unknown, year is estimated": ["UUE"],
        "UUU - Day, month and year are unknown":      ["UUU"],        
        "EEA - Day and month are estimated, year is accurate" : ["EEA"],

        "Short term crisis, emergency or transitional accommodation facility" : [
            "Short term crisis, emergency or transitional accommodation f"
        ],

        "Other specialised community residential": [
            "Other specialised community residential"            
        ],
        
        "Boarding house/private hotel" : ["Boarding house/private rental"],
        "None/homeless/public place" : ["None/homeless/public space"],
        
        "Alcohol and other drug treatment service": ["Alcohol & other drug treatment"],
        "Other community/health care service" : ["Other community/health service"],

        "Change in main treatment type" : ["Change in the main treatment type"],
        "Change in delivery setting" : ["Change in the delivery setting"],
        "No previous treatment received" : ["No treatment"],

        "Vietnam" : ["Viet Nam"],
        "Serbia" : ["Serbia and Montenegro"],
        "Arabic" : ["Arabic (Including Lebanese)"],
        "British Antarctic" : ["British Antarctic Territory"],
        "Myanmar" : ["Burma (Myanmar)", "Burma (Republic of the Union of Myanmar)"],
        #Prev treatment
        #"-" : ["Not Stated"],
        "Information and education only"  :["Information and Education only"],

        # CASE SENSITIVE STUFF 
        "Outreach setting" : ["Outreach Setting"],
        "Private residence" : ["Private Residence", "Rented private house or flat", "Privately owned house or flat",
                             "Rented public house or flat"
        ], 

        "Friend(s)/parent(s)/relative(s) and child(ren)" : ["Friend(s)/parent(s)/relative(s) and chil(ren)"],
        "Spouse/partner and child(ren)" : ["Spouse/partner and Child(ren)"],
        "Medical Practitioner": ["Medical practitioner"],
        "Withdrawal management (detoxification)" : ["Withdrawal Management (detoxification)", "Withdrawl management (detoxification)"],        
        "Alone" : ["alone"],
        "Other relative(s)" : ["Other Relative(s)"], # TODO check me Family memner/friend eqiuivalemtr
        "Family member/friend": ["Family member/Friend"],
        "Residential treatment facility" : ["Residential Treatment Facility"],
        #:["Sniffs (powder)"]
        "Correctional service" : ["Correctional Service"]


        # "" : [""],
        # "" : [""],
    }
}


mds_aliases['headers'][M['ID']]      = ["PAT ID", "PID"]
mds_aliases['headers'][M['FNAME']]   = ["First Name", "Firstname"]
mds_aliases['headers'][M['LNAME']]   = ["Last Name"]
mds_aliases['headers'][M['PDC']]     = ["PDC"]
mds_aliases['headers'][M['SEX']]     = ["SEX"]
mds_aliases['headers'][M['DOB']]     = ["Date of birth"]
mds_aliases['headers'][M['DAI']]     = ["DOB ACCURACY", "Date accuracy indicator (for DoB)"]
mds_aliases['headers'][M['PCODE']]   = ["POSTCODE", "Postcode - Australian"]
mds_aliases['headers'][M['TRDLVSTG']] = ["SETTING"]
mds_aliases['headers'][M['METHOD']]   = ["USE", "Method of use for principal drug of concern"]
mds_aliases['headers'][M['INJ_USE']]  = ["INJECTION", "Injecting drug status"]
mds_aliases['headers'][M['MTT']]      = ["TREAT", "Main treatment type (MTT)"]
mds_aliases['headers'][M['MENT_HEL']] = ["MENTAL HEALTH", "Mental health (Diagnosed with a mental illness)"]
mds_aliases['headers'][M['PDC']]      = ["DRUG", "PDC"]
mds_aliases['headers'][M['USACC']]    = ["ACCOM", "Usual accommodation type"]
mds_aliases['headers'][M['PREV_AOD']] = ["PREVIOUS TREATMENT", "Previous AOD treatment"]
mds_aliases['headers'][M['LIVAR']]    = ["LIVING"]
mds_aliases['headers'][M['REAS_CESS']]= ["CESSATION"]
mds_aliases['headers'][M['PLANG']]    = ["LANGUAGE"]
mds_aliases['headers'][M['COB']]      = ["COUNTRY"]
mds_aliases['headers'][M['SLK']]      = ["SLK581"]
mds_aliases['headers'][M['ATSI']]     = ["INDIG STATUS"]
mds_aliases['headers'][M['CLNT_TYP']] = ["CLIENT"]
mds_aliases['headers'][M['SRC_REF']]  = ["SOURCE"]
mds_aliases['headers'][M['COMM_DATE']]= ["ENROLMENT", "Commencement Date", "Commencement date"]
mds_aliases['headers'][M['END_DATE']] = ["DISCHARGE"]
