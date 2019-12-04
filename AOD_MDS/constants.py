
# schemaObj['definitions']['episode']['properties']['Principle drug of concern']['description']

# TODO: Build this from the schema.json file. The "description" for each property is the key and the 
# key of each property (in schema.json), is the value in the below dict.
MDS = {
    "ID": "ID",
    "SEX": "Sex",
    "COMM_DATE" : "Commencement date",
    "DOB" : 'DOB', #Date of Birth",
    "SLK": "SLK 581",
    "FNAME": "First name",
    "LNAME": "Surname",
    "DAI": "Date accuracy indicator",
    "END_DATE" : "End date",
    "METHOD" : "Method of use for PDC",
    "PDC" : "Principle drug of concern",
    "INJ_USE" : "Injecting drug use status",
    "CLNT_TYP" : "Client type",
    "COB": "Country of birth",
    "ATSI": "Indigenous status",
    "PLANG": "Preferred language",
    "PCODE": "Postcode (Australian)",
    "MTT": "Main treatment type",
    "LIVAR": "Living arrangements",
    "USACC": "Usual accommodation",
    "TRDLVSTG": "Treatment delivery setting",
    "SRC_REF": "Source of referral",
    "MENT_HEL": "Mental health",
    "PREV_AOD": "Previous alcohol and other drug treatment received", #Previous AOD treatment",
    "REAS_CESS": "Reason for cessation"
}

MDS_Dates = ("DOB", "COMM_DATE", "END_DATE")

MDS_ST_FLD = 'O'+MDS['COMM_DATE']
MDS_END_FLD = 'O'+MDS['END_DATE']

