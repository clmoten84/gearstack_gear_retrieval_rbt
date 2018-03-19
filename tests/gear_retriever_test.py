# ------------------------------------------------------------------------
#
# Module: gear_retriever_test.py
# Created By: coreym
# Created On: 2018/Mar/09
#
# Description: Unit tests for GearRetriever functions
#
# ------------------------------------------------------------------------

import unittest
import configUtils.config_utils as config_utils
import logUtils.log_utils as log_utils
from retrievers.gear_retriever import GearRetriever

class GearRetrieverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configs = config_utils.fetch_bot_config(env='local')
        cls.retriever = GearRetriever(amazon_config=configs['amazon_config'],
                                      app_db_config=configs['db_config']['app_db_props'],
                                      exclusion_keys=config_utils.fetch_data_config('excluded_keywords'))

    @classmethod
    def tearDownClass(cls):
        pass

    """ Tests search_items() function """
    def test_search_items(self):
        # Fetch a node to search items for
        search_node = config_utils.fetch_data_config(config_name='computer_recording')[0]
        items = self.retriever.search_items(browse_node_id=search_node, price_limit=10000)
        print len(items)
        self.assertIsNotNone(items)
        self.assertTrue(len(items) > 0)

    """ Tests clean_html() function """
    def test_clean_html(self):
        html_string = u'<p><u>Some random text!</u></p>'
        clean_string = self.retriever.clean_html(html_string)
        print clean_string


""" Execute tests """
if __name__ == '__main__':
    # Initialize a root logger so logging works during tests
    root_logger = log_utils.init_root_logger(logger_name="gear_rbt_logger",
                                             log_path="../log/gear_rbt.log",
                                             log_level="DEBUG")

    try:
        # Create test suite and execute
        suite = unittest.TestLoader().loadTestsFromTestCase(GearRetrieverTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
