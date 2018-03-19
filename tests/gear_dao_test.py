# ------------------------------------------------------------------------
#
# Module: gear_dao_test.py
# Created By: coreym
# Created On: 2018/Mar/09
#
# Description: Unit tests for Gear DAO functions
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from models.gear import Gear
from dao.gear_dao import GearDAO


class GearDAOTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_db_config = config_utils.fetch_bot_config(env='local')['db_config']['app_db_props']
        cls.dao = GearDAO(app_db_config)

    @classmethod
    def tearDownClass(cls):
        del cls.dao

    """ Tests save, fetch, delete functions of DAO """
    def test_save_fetch_delete(self):
        # Create a test Gear instance to persist
        gear = Gear(name='Test Gear',
                    description='Some piece of gear.',
                    thumb_url='http://some.path.to.thumbnail',
                    amazon_link='http://some.amazon.link',
                    image_url='http://some.path.to.gear.image',
                    manufacturer='Propellerhead',
                    type_id=11973721,
                    features='Awesome;Amazing;Cool')

        # Save gear instance to database
        rec_id = self.dao.save_gear(gear)
        self.assertIsNotNone(rec_id)
        print rec_id

        # Fetch gear instance by id
        fetched_rec = self.dao.fetch_gear_by_id(rec_id)
        self.assertIsNotNone(fetched_rec)
        self.assertEquals(fetched_rec.name, 'Test Gear')

        # Fetch gear instance by name
        fetched_rec = self.dao.fetch_gear_by_name('Test Gear')
        self.assertIsNotNone(fetched_rec)

        # Delete gear instance
        self.dao.delete_gear(rec_id)
        fetched_rec = self.dao.fetch_gear_by_id(rec_id)
        self.assertIsNone(fetched_rec)

""" Execute tests """
if __name__ == '__main__':
    # Initialize a root logger here so logging works during tests
    root_logger = log_utils.init_root_logger(logger_name="gear_rbt_logger",
                                             log_path="../log/gear_rbt.log",
                                             log_level='DEBUG')
    try:
        # Create test suite and execute
        suite = unittest.TestLoader().loadTestsFromTestCase(GearDAOTest)
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
