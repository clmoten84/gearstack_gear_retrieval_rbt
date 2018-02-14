# ------------------------------------------------------------------------
#
# Module: log_utils.py
# Created By: coreym
# Created On: 2018/Feb/10
#
# Description: Handles logging to application log
#
# ------------------------------------------------------------------------

import logging
import os

""" Initializes logger to be used as root logger for application. """
def init_root_logger(log_level="DEBUG"):
    logger = logging.getLogger("gearstack_rbt")
    logger.setLevel(_set_log_level(log_level))
    file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), '../log/gear_retriever.log'),
                                       mode='w')
    file_handler.setLevel(_set_log_level(log_level))
    formatter = logging.Formatter('%(asctime)s - [%(name)s - %(module)s : %(funcName)s] - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

""" Closes argument logger by closing and removing all handler from logger. """
def close_logger(logger):
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

""" Returns log level given log level name. """
def _set_log_level(log_level=None):
    if log_level.lower() == 'debug':
        return logging.DEBUG
    if log_level.lower() == 'info':
        return logging.INFO
    if log_level.lower() == 'error':
        return logging.ERROR
    if log_level.lower() == 'warning':
        return logging.WARNING
    if log_level.lower() == 'critical':
        return logging.CRITICAL
    if log_level is None:
        return logging.NOTSET

