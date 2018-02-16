# ------------------------------------------------------------------------
#
# Module: db_utils_test.py
# Created By: coreym
# Created On: 2018/Feb/13
#
# Description: Unit tests for db_utils module classes and functions
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from dbUtils.db_utils import DBUtils

class DBUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_configs = config_utils.fetch_config(env="local")['db_config']
        cls.db_utils = DBUtils(db_configs)

    @classmethod
    def tearDownClass(cls):
        cls.db_utils.close_db_connections()
        del cls.db_utils

    """ Tests that a connection could be made to application database. 
        Just runs a query to get Postgres version. """
    def test_app_db_conn(self):
        # Create a cursor from DB connection
        with self.db_utils.app_db_conn.cursor() as db_cursor:
            db_cursor.execute('SELECT version()')
            db_version = db_cursor.fetchone()
            self.assertIsNotNone(db_version)
            print db_version


""" MAIN - execute tests """
if __name__ == '__main__':
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(DBUtilsTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
