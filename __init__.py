import os
import json
import logging
import logging.config

# from .IndexFile import IndexFile
# from .Staff import Staff


default_path = 'config\\logging.json'
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
#logger.info('Completed configuring logger()!')