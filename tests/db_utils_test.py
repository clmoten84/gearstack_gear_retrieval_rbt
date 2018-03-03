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
import dbUtils.db_utils as db_utils

class DBUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_configs = config_utils.fetch_config(env="local")['db_config']

    @classmethod
    def tearDownClass(cls):
        del cls.db_configs

    """ Tests open_connection static function of db_utils. """
    def test_open_connection(self):
        # Test open connection function
        db_version = None
        bot_db_props = self.db_configs['bot_db_props']
        db_conn = db_utils.open_db_connection(db_configs=bot_db_props)
        with db_conn.cursor() as cursor:
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            self.assertIsNotNone(db_version)
            print db_version

        # Close database connection
        db_utils.close_db_connection(db_conn)


""" MAIN - execute tests """
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(DBUtilsTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
