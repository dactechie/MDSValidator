import os
import json
import logging
import logging.config


# The CWD is the venv's PYTHONPATH when running from Excel VBA, 
# so it looks for config/ etc at mds/Scripts/... If it doesn't find a config dir, 
# we change the cwd to the root of the project and everything is just 'dandy'
if not os.path.exists(os.path.join(os.getcwd(), "config")):
    os.chdir(f"..{os.sep}..")

root_dir = os.getcwd()

default_path = os.path.join(root_dir, f"config{os.sep}logging.json")
default_level = logging.INFO
env_key = 'LOG_CFG'

path = default_path
value = os.getenv(env_key, None)
if value:
    path = value
if os.path.exists(path):
    with open(path, 'rt') as f:
        config = json.load(f)
    print("***************using config file for setting up logger")
    logging.config.dictConfig(config)
else:
    logging.basicConfig(level=default_level,
                        filename=default_path,
                        format="%(asctime)s - %(levelname)s - %(message)s")

# Log that the logger was configured
logger = logging.getLogger(__name__)

logger.info('Completed configuring logger()!')
