# ------------------------------------------------------------------------
#
# Module: geartype_dao_test.py
# Created By: coreym
# Created On: 2018/Mar/07
#
# Description: Unit tests for GearTypeDAO
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from dao.geartype_dao import GearTypeDAO
from models.gear_type import GearType


class GearTypeDAOTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_db_configs = config_utils.fetch_bot_config(env='local')['db_config']['app_db_props']
        cls.dao = GearTypeDAO(app_db_configs=app_db_configs)

    @classmethod
    def tearDownClass(cls):
        del cls.dao

    """ Tests insert, fetch, and delete functions of DAO class. """
    def test_insert_fetch_delete(self):
        # Create a test GearType instance to persist
        gear_type = GearType(amazon_node_id=123456,
                             name='Test Gear Type',
                             parent_node_id=None,
                             is_leaf_node=True)

        # Insert test GearType instance
        ret_id = self.dao.insert_geartype(gear_type)
        self.assertIsNotNone(ret_id)
        self.assertEquals(ret_id, 123456)

        # Fetch record by id
        fetched_by_id = self.dao.fetch_geartype_by_id(type_id=ret_id)
        self.assertIsNotNone(fetched_by_id)
        self.assertEquals(fetched_by_id.amazon_node_id, 123456)

        # Fetch record by name
        fetched_by_name = self.dao.fetch_geartype_by_name(name='Test Gear Type')
        self.assertIsNotNone(fetched_by_name)
        self.assertEquals(fetched_by_name.amazon_node_id, 123456)

        # Delete record
        self.dao.delete_geartype(type_id=ret_id)
        self.assertIsNone(self.dao.fetch_geartype_by_id(type_id=ret_id))


# Execute tests
if __name__ == '__main__':
    root_logger = None
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(logger_name="gearstack_rbt",
                                                 log_path='../log/geartype_rbt.log',
                                                 log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(GearTypeDAOTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
