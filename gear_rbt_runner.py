# ------------------------------------------------------------------------
#
# Module: gear_rbt_runner.py
# Created By: coreym
# Created On: 2018/Mar/03
#
# Description:  Runner for retrieving gear data from Amazon PAAPI
#               and persisting to database.
#
# ------------------------------------------------------------------------

import getopt
import sys
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from retrievers.gear_retriever import GearRetriever

""" Main function to execute retrieval of gear items from Amazon """
def main(argv):
    # Gather command line args
    env = None
    log_level = None
    item_type = None
    usage = "gear_rbt_runner.py --env <local|dev|prod> --log_level <info|debug|warning|error> " \
            "--item_type <item-type-name>"

    try:
        opts, args = getopt.getopt(argv, "h", ["env=", "log_level=", "item_type="])
    except getopt.GetoptError:
        print ('An invalid argument was specified!')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print (usage)
            sys.exit(0)
        elif opt == '--env':
            env = arg
        elif opt == '--log_level':
            log_level = arg
        elif opt == '--item_type':
            item_type = arg

    # Validate command line args
    try:
        # env arg
        if env.lower() not in ('local', 'dev', 'prod'):
            print ('An invalid value {0} was specified for arg [--env]'.format(env))
            print (usage)
            sys.exit(2)

        # log_level arg
        if log_level.lower() not in ('info', 'debug', 'warning', 'error', 'critical'):
            print ('An invalid value {0} was specified for arg [--log_level]'.format(log_level))
            print (usage)
            sys.exit(2)
    except AttributeError:
        print ('An invalid argument was specified!')
        print (usage)
        sys.exit(2)

    # Create logger and log options specified
    logger = log_utils.init_root_logger(logger_name="gear_rbt_logger",
                                        log_path='../log/gear_rbt.log',
                                        log_level=log_level)
    logger.info('Gearstack Gear Bot')
    logger.info('Environment: {0}'.format(env.upper()))
    logger.info('Log Level: {0}'.format(log_level.upper()))

    # Fetch configuration data for specified environment
    bot_configs = config_utils.fetch_bot_config(env)
    types = config_utils.fetch_data_config('cat_data_keys')

    # Have to validate item_type arg here because config_utils is needed to validate this arg
    if item_type not in types:
        print ('An invalid item type {0} was specified'.format(item_type))
        sys.exit(2)

    # Instantiate gear retriever instance
    gear_retriever = GearRetriever(amazon_config=bot_configs['amazon_config'],
                                   app_db_config=bot_configs['db_config']['app_db_props'],
                                   exclusion_keys=config_utils.fetch_data_config('excluded_keywords'))

    # Fetch nodes to search using item_type argument
    nodes_to_search = config_utils.fetch_data_config(item_type)

    # Loop through nodes_to_search list and execute amazon API search
    # and item save
    try:
        for node in nodes_to_search:
            fetched_items = gear_retriever.search_items(browse_node_id=node)
            gear_retriever.save_gear(item_list=fetched_items, browse_node=node)
    except Exception:
        logger.exception('Gear Retriever bot encountered an exception during execution!')
    finally:
        log_utils.close_logger(logger)


""" Execute main function """
if __name__ == '__main__':
    main(sys.argv[1:])
