# ------------------------------------------------------------------------
#
# Module: geartype_retriever_test.py
# Created By: coreym
# Created On: 2018/Feb/18
#
# Description: Unit tests for CategoryRetriever class
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from retrievers.geartype_retriever import GearTypeRetriever

class GearTypeRetrieverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        all_configs = config_utils.fetch_bot_config(env='local')
        amazon_configs = all_configs['amazon_config']
        bot_db_configs = all_configs['db_config']['bot_db_props']
        app_db_configs = all_configs['db_config']['app_db_props']
        cls.cat_retriever = GearTypeRetriever(amazon_config=amazon_configs,
                                              bot_db_configs=bot_db_configs,
                                              app_db_configs=app_db_configs)

    @classmethod
    def tearDownClass(cls):
        del cls.cat_retriever

    """ Tests node_lookup function of CategoryRetriever class """
    def test_node_lookup(self):
        # Fetch node id to use from config and perform node lookup with it
        result = self.cat_retriever.node_lookup(11971381)

        # Do some assertions here to verify success
        self.assertIsNotNone(result)
        self.assertEquals(str(result.name), 'Electric Guitars')

    """ Tests save_geartypes() function of GearTypeRetriever class """
    def test_save_geartypes(self):
        # Grab a list of node_ids from config file
        guitar_nodes = config_utils.fetch_data_config('guitars')
        print ('Fetching the following nodes: {0}'.format(guitar_nodes))

        # Execute function of test
        self.cat_retriever.save_geartypes(node_ids=guitar_nodes)


""" Execute unit tests. """
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger so logging works inside CategoryRetriever class
        root_logger = log_utils.init_root_logger(logger_name="gearstack_rbt",
                                                 log_path='../log/geartype_rbt.log',
                                                 log_level="DEBUG")

        # Execute unit tests
        suite = unittest.TestLoader().loadTestsFromTestCase(GearTypeRetrieverTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
