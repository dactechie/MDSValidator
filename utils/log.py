
from logger import logger


def log_results(verrors, warnings, header_warnings):
    
    logger.info(f"\n {10*'-'}   Errors {10*'-'}")
    for v in verrors.values():
        logger.info(v)
        logger.info("")

    if any(warnings):
        logger.info(f"\n {10*'-'},  Warnings ,{10*'-'}")
        logger.info(warnings)

    if (header_warnings):
        logger.info(f"\n header warnings {header_warnings}")
