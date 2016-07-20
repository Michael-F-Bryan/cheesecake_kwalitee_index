"""
Miscellaneous utility functions, classes, constants and decorators.
"""

import logging
import sys



def get_logger(name, log_file, log_level=None):
    """
    Get a logger object which is set up properly with the correct formatting,
    logfile, etc.

    Parameters
    ----------
    name: str
        The __name__ of the module calling this function.
    log_file: str
        The filename of the file to log to.

    Returns
    -------
    logging.Logger
        A logging.Logger object that can be used to log to a common file.
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level or logging.INFO)

    if log_file == 'stdout':
        handler = logging.StreamHandler(sys.stdout)
    elif log_file == 'stderr':
        handler = logging.StreamHandler(sys.stderr)
    else:
        handler = logging.FileHandler(log_file)

    if not len(logger.handlers):
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s',
            datefmt='%Y/%m/%d %I:%M:%S %p'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
