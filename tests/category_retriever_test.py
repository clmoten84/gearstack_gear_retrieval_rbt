# ------------------------------------------------------------------------
#
# Module: category_retriever_test.py
# Created By: coreym
# Created On: 2018/Feb/18
#
# Description: Unit tests for CategoryRetriever class
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from retrievers.category_retriever import CategoryRetriever

class CategoryRetrieverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        all_configs = config_utils.fetch_config(env='local')
        amazon_configs = all_configs['amazon_config']
        bot_db_configs = all_configs['db_config']['bot_db_props']
        cls.cat_retriever = CategoryRetriever(amazon_config=amazon_configs, bot_db_configs=bot_db_configs)

    @classmethod
    def tearDownClass(cls):
        del cls.cat_retriever

    """ Tests node_lookup function of CategoryRetriever class """
    def test_node_lookup(self):
        # Fetch node id to use from config and perform node lookup with it
        node_id = self.cat_retriever.amazon_config['cat_starter_node']
        result = self.cat_retriever.node_lookup(node_id)

        # Do some assertions here to verify success
        self.assertIsNotNone(result)
        self.assertEquals(str(result.name).upper(), 'PRODUCTS')


""" Execute unit tests. """
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger so logging works inside CategoryRetriever class
        root_logger = log_utils.init_root_logger(log_level='DEBUG')

        # Execute unit tests
        suite = unittest.TestLoader().loadTestsFromTestCase(CategoryRetrieverTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
