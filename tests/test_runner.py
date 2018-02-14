# ------------------------------------------------------------------------
#
# Module: test_runner.py
# Created By: coreym
# Created On: 2018/Feb/13
#
# Description: Runs all unit test cases for application
#
# ------------------------------------------------------------------------

import unittest
import logUtils.log_utils as log_utils
from config_utils_test import ConfigUtilsTest
from db_utils_test import DBUtilsTest

if __name__ == '__main__':
    try:
        # Initialize root logger so that the logging works during tests
        root_logger = log_utils.init_root_logger(log_level="DEBUG")

        # Define list of test case classes to run
        tests = [ConfigUtilsTest, DBUtilsTest]
        suites_list = []

        # Initialize test loader
        loader = unittest.TestLoader()

        # Loop through test lists to load tests from test cases
        for test in tests:
            suites_list.append(loader.loadTestsFromTestCase(test))

        # Create big_suite of all test suites and execute it
        big_suite = unittest.TestSuite(suites_list)
        unittest.TextTestRunner(verbosity=2).run(big_suite)
    finally:
        # Close root logger
        if root_logger:
            log_utils.close_logger(root_logger)
