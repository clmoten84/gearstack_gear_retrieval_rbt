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
    browse_node = None
    usage = "gear_rbt_runner.py --env <local|dev|prod> --log_level <info|debug|warning|error> " \
            "--browse_node <browse_node_id>"

    try:
        opts, args = getopt.getopt(argv, "h", ["env=", "log_level=", "browse_node="])
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
        elif opt == '--browse_node':
            browse_node = arg

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

        # browse_node arg
        browse_node = int(browse_node)
    except (AttributeError, ValueError):
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
    logger.info('Amazon Browse Node: {0}'.format(browse_node))

    # Fetch configuration data for specified environment
    bot_configs = config_utils.fetch_bot_config(env)

    # Instantiate gear retriever instance
    gear_retriever = GearRetriever(amazon_config=bot_configs['amazon_config'],
                                   app_db_config=bot_configs['db_config']['app_db_props'],
                                   exclusion_keys=config_utils.fetch_data_config('excluded_keywords'))

    # Loop through nodes_to_search list and execute amazon API search
    # and item save
    try:
        fetched_items = gear_retriever.search_items(browse_node_id=browse_node)
        gear_retriever.save_gear(item_list=fetched_items, browse_node=browse_node)

        logger.info("Finished DB population for browse node {0}!!!".format(browse_node))
    except Exception:
        logger.exception('Gear Retriever bot encountered an exception during execution!')
    finally:
        log_utils.close_logger(logger)


""" Execute main function """
if __name__ == '__main__':
    main(sys.argv[1:])
