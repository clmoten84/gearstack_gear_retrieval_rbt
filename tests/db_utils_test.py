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

class DBUtilsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass


""" MAIN - execute tests """
if __name__ == '__main__':
    try:
        # Initialize root logger here for logging to work during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define and execute test suite
        suite = unittest.TestLoader().loadTestsFromTestCase(DBUtilsTest)
        unittest.TextTestRunner(verbosity=2).run(suite)

    finally:
        if root_logger:
            log_utils.close_logger(root_logger)
