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

    """ Fetch database config for local environment """
    def test_fetch_db_config(self):
        # Retrieve config props
        db_config = config.fetch_bot_config(env='local')['db_config']

        # Assert an application database prop
        self.assertEquals(db_config['app_db_props']['db_name'], 'gearstack')

        # Assert a log database prop
        self.assertEquals(db_config['bot_log_db_props']['db_name'], 'gearstack_bot_logs')

        # Assert a bot database prop
        self.assertEquals(db_config['bot_db_props']['db_name'], 'gearstack_bot')

    """ Fetch Amazon config for local environment """
    def test_fetch_amazon_config(self):
        # Retrieve config props
        amazon_config = config.fetch_bot_config(env='local')['amazon_config']

        # Assert Amazon prop
        self.assertEquals(amazon_config['associate_tag'], 'gearstack-20')
        self.assertEquals(amazon_config['cat_starter_node'], 11965861)

    """ Fetch configuration properties for bogus environment """
    def test_fetch_config_fail(self):
        # Attempt to retrieve config props from bogus environment
        # Use assertRaises as context manager here to avoid failure due to exception
        with self.assertRaises(InvalidEnvException):
            config.fetch_bot_config(env='bogus')

    """ Tests fetch_cat_nodes() function of config_utils module """
    def test_fetch_cat_nodes(self):
        # Attempt to retrieve cat_nodes for a category
        nodes = config.fetch_data_config('guitars')
        self.assertIsNotNone(nodes)
        self.assertTrue(len(nodes) == 4)


""" MAIN - execute tests"""
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ConfigUtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
