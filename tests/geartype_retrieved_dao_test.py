# ------------------------------------------------------------------------
#
# Module: geartype_retrieved_dao_test.py
# Created By: coreym
# Created On: 2018/Feb/24
#
# Description: Units tests for CategoryRetrieverDAO class
#
# ------------------------------------------------------------------------

import unittest
import configUtils.config_utils as config_utils
import logUtils.log_utils as log_utils
from dao.geartype_retrieved_dao import GearTypeRetrievedDAO
from models.gear_type_retrieved import GearTypeRetrieved


class GearTypeRetrievedDAOTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        bot_db_configs = config_utils.fetch_bot_config(env='local')['db_config']['bot_db_props']
        cls.dao = GearTypeRetrievedDAO(bot_db_configs=bot_db_configs)

    @classmethod
    def tearDownClass(cls):
        del cls.dao

    """  Tests inserting, fetching, and deleting functions of DAO class. """
    def test_insert_fetch_delete(self):
        # Create an instance of CategoriesRetrieved model
        gear_type_retrieved = GearTypeRetrieved(amazon_node_id=123456)

        # Insert instance of model
        ret_id = self.dao.insert_geartype_retrieved(gear_type_retrieved=gear_type_retrieved)
        self.assertIsNotNone(ret_id)
        self.assertEquals(ret_id, 123456)

        # Fetch GearTypeRetrieved record by id
        fetched_by_id = self.dao.fetch_geartype_retrieved_by_id(node_id=ret_id)
        self.assertIsNotNone(fetched_by_id)
        self.assertEquals(fetched_by_id.amazon_node_id, 123456)

        # Delete record from database
        self.dao.delete_geartype_retrieved(node_id=ret_id)
        self.assertIsNone(self.dao.fetch_geartype_retrieved_by_id(node_id=ret_id))



""" MAIN - Execute unit tests. """
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(GearTypeRetrievedDAOTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
