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

import psycopg2
import logging
import logUtils.log_utils as log_utils

class DBUtils:
    def __init__(self, db_configs):
        # Create logger to use for this module
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(DBUtils.__name__))

        # Open connection to application database
        try:
            self.app_db_conn = self._open_db_connection(db_configs['app_db_props'])
        except psycopg2.DatabaseError as db_err:
            self.logger.exception('An error occurred during database connection attempt!')
            log_utils.close_logger(self.logger)
            raise db_err

    """ Opens a connection to a database using argument db configuration """
    def _open_db_connection(self, db_config):
        conn = psycopg2.connect(host=db_config['db_host'], database=db_config['db_name'],
                                 user=db_config['db_user'], password=db_config['db_pass'],
                                 port=db_config['port'])
        self.logger.info('Connection opened to database: {0}'.format(db_config['db_name']))
        return conn

    """ Closes all open database connections """
    def close_db_connections(self):
        # Close application database connection
        if self.app_db_conn:
            self.app_db_conn.close()
            self.logger.info('ALL database connections closed!')
