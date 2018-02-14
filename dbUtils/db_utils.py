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

class DBUtils:
    def __init__(self, db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(DBUtils.__name__))
        pass

    """ Opens a connection to a database using argument db configuration """
    def _open_db_connection(self, db_config):
        pass

    """ Closes all open database connections """
    def close_db_connections(self):
        pass
