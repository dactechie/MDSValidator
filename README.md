# MDSValidator
Schema and Logic validation for AOD MDS dataset (based on National Minimum Dataset)

## Setup

After cloning, cd into the project directory and run
```
> python -m venv .venv        (to create the virtual environment)
> pip install -r requirements.txt  (to install the dependencies within the environment)
```

## Running the validator
1. Drop your input .csv MDS file to be checked into the ./input folder
2. Then to do basic MDS checks run :
`> python MDSDataFileProcessor.py`

This will pick up the latest file in the input folder. 

Alternatively you can specify commandline options. 
You can see the help menu by typing 
` > python MDSDataFileProcessor.py --help `

```
Usage: MDSDataFileProcessor.py [OPTIONS]`

Options:
  -d, --data_file TEXT            Default: use the latest .csv file in the
                                  input folder.
  -a, --all_eps / -c, --closed_only
                                  Validate only closed episodes. Default is to
                                  validate all episodes  [default: True]
  -e, --errors_only BOOLEAN       Output only the rows with errors.  [default:
                                  False]
  -t, --start_date [%Y-%m-%d]     The number of the starting month of the
                                  reporting period . Eg.: 2019-07-01
  -p, --program [TSS|Arcadia-Resi|Althea|Other]
                                  Some logic rules are specific to a
                                  team.Default setting is to just apply just
                                  MDS rules.  [default: TSS]
  -r, --reporting_period [12|6|3|1]
                                  reporting period window.  [default: 3]
  -s, --nostrict / -S, --strict   Accept/Reject imperfect data files with
                                  known aliases.
                                  1: reject (flag as errors)
                                  [default: False]
  --help                          Show this message and exit.
```
