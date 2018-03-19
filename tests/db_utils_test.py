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
        cls.db_configs = config_utils.fetch_bot_config(env="local")['db_config']

    @classmethod
    def tearDownClass(cls):
        del cls.db_configs

    """ Tests open_connection static function of db_utils. """
    def test_open_connection(self):
        # Test open connection to bot database
        db_version = None
        bot_db_props = self.db_configs['bot_db_props']
        bot_db_conn = db_utils.open_db_connection(db_configs=bot_db_props)
        with bot_db_conn.cursor() as cursor:
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            self.assertIsNotNone(db_version)
            print db_version

        # Test open connection to app database
        db_version = None
        app_db_props = self.db_configs['app_db_props']
        app_db_conn = db_utils.open_db_connection(db_configs=app_db_props)
        with app_db_conn.cursor() as cursor:
            cursor.execute('SELECT version()')
            db_version = cursor.fetchone()
            self.assertIsNotNone(db_version)
            print db_version

        # Close database connections
        db_utils.close_db_connection(bot_db_conn)
        db_utils.close_db_connection(app_db_conn)


""" MAIN - execute tests """
if __name__ == '__main__':
    # Define and execute test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(DBUtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
