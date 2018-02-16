# ------------------------------------------------------------------------
#
# Module: config_utils_test.py
# Created By: coreym
# Created On: 2018/Feb/11
#
# Description: Unit tests for config_utils module
#
# ------------------------------------------------------------------------

import unittest
import os
import configUtils.config_utils as config
from custom_errs.invalid_env_err import InvalidEnvException


class ConfigUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    """ Fetch configuration properties for local environment """
    def test_fetch_config(self):
        # Retrieve config props for local environment
        local_props = config.fetch_config(env='local')

        # Assertions
        self.assertEquals(local_props['db_config']['app_db_props']['db_host'], 'localhost')
        self.assertEquals(local_props['db_config']['app_db_props']['db_name'], 'gearstack')
        self.assertEquals(local_props['db_config']['app_db_props']['db_user'], 'gearstack_app')
        self.assertEquals(local_props['db_config']['app_db_props']['db_pass'], 'P@$$w)rd')
        self.assertEquals(local_props['db_config']['app_db_props']['port'], 5432)

    """ Fetch configuration properties for bogus environment """
    def test_fetch_config_fail(self):
        # Attempt to retrieve config props from bogus environment
        # Use assertRaises as context manager here to avoid failure due to exception
        with self.assertRaises(InvalidEnvException):
            config.fetch_config(env='bogus')


""" MAIN - execute tests"""
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigUtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
