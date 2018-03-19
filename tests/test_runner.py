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
from geartype_retriever_test import GearTypeRetrieverTest
from geartype_retrieved_dao_test import GearTypeRetrievedDAOTest
from geartype_dao_test import GearTypeDAOTest

if __name__ == '__main__':
    try:
        # Initialize both loggers so that the logging works during tests
        geartype_logger = log_utils.init_root_logger(logger_name="gearstack_rbt",
                                                 log_path="../log/geartype_rbt.log",
                                                 log_level="DEBUG")

        gear_logger = log_utils.init_root_logger(logger_name="gear_rbt_logger",
                                                 log_path="../log/gear_rbt.log",
                                                 log_level="DEBUG")

        # Define list of test case classes to run
        tests = [ConfigUtilsTest, DBUtilsTest, GearTypeRetrieverTest,
                 GearTypeRetrievedDAOTest, GearTypeDAOTest]
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
        if geartype_logger:
            log_utils.close_logger(geartype_logger)

        if gear_logger:
            log_utils.close_logger(gear_logger)
