# ------------------------------------------------------------------------
#
# Module: db_utils.py
# Created By: coreym
# Created On: 2018/Feb/13
#
# Description: Contains a class (DBUtils) for handling application
#              persistence.
#
# ------------------------------------------------------------------------

import psycopg2 as psycopg2
import logging
import logUtils.log_utils as log_utils
from models.gear_type import GearType

# Define logger at module level
logger = logging.getLogger('gearstack_rbt.db_utils')

""" Opens a connection to a database using argument db configuration. """
def open_db_connection(db_configs):
    try:
        conn = psycopg2.connect(host=db_configs['db_host'],
                                database=db_configs['db_name'],
                                user=db_configs['db_user'],
                                password=db_configs['db_pass'],
                                port=db_configs['port'])
        logger.info('Connection established to database: {0}'.format(db_configs['db_name']))
        return conn
    except psycopg2.DatabaseError as db_err:
        logger.exception('An error occurred during database connection attempt!')
        log_utils.close_logger(logger)
        raise db_err

def close_db_connection(conn):
    if conn:
        conn.close()
        logger.info('Connection to database closed!')