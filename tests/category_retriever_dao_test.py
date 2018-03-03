# ------------------------------------------------------------------------
#
# Module: category_retriever_dao_test.py
# Created By: coreym
# Created On: 2018/Feb/24
#
# Description: Units tests for CategoryRetrieverDAO class
#
# ------------------------------------------------------------------------

import unittest
import configUtils.config_utils as config_utils
import logUtils.log_utils as log_utils
from dao.categories_retrieved_dao import CategoriesRetrievedDAO
from models.categories_retrieved import CategoryRetrieved


class CategoryRetrieverDAOTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bot_db_configs = config_utils.fetch_config(env='local')['db_config']['bot_db_props']
        cls.dao = CategoriesRetrievedDAO(bot_db_configs=bot_db_configs)

    @classmethod
    def tearDownClass(cls):
        del cls.dao

    """  Tests inserting, fetching, and deleting functions of DAO class. """
    def test_insert_fetch_delete(self):
        # Create an instance of CategoriesRetrieved model
        category = CategoryRetrieved(amazon_node_id=123456,
                                     name='Test Category',
                                     parent_node_id=None,
                                     is_leaf_node=False)

        # Insert instance of model
        ret_id = self.dao.insert_category(category_retrieved=category)
        self.assertIsNotNone(ret_id)
        self.assertEquals(ret_id, 123456)

        # Fetch record from database by id and name
        fetched_by_name = self.dao.fetch_category_by_name(name='Test Category')
        self.assertIsNotNone(fetched_by_name)
        self.assertEquals(fetched_by_name.amazon_node_id, 123456)
        self.assertEquals(fetched_by_name.name, 'Test Category')

        fetched_by_id = self.dao.fetch_category_by_id(id=ret_id)
        self.assertIsNotNone(fetched_by_id)
        self.assertEquals(fetched_by_id.amazon_node_id, 123456)
        self.assertEquals(fetched_by_id.name, 'Test Category')

        # Delete record from database
        self.dao.delete_category(node_id=ret_id)
        self.assertIsNone(self.dao.fetch_category_by_id(id=ret_id))



""" MAIN - Execute unit tests. """
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(CategoryRetrieverDAOTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
