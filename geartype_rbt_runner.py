# ------------------------------------------------------------------------
#
# Module: geartype_rbt_runner.py
# Created By: coreym
# Created On: 2018/Mar/06
#
# Description: Runner for retrieving gear category data from Amazon PAAPI
#
# ------------------------------------------------------------------------

import getopt
import sys
import logUtils.log_utils as log_utils
import configUtils.config_utils as config_utils
from retrievers.geartype_retriever import GearTypeRetriever

""" Main function to execute gear type retrieval logic. """
def main(argv):
    # Gather command line args
    env = None
    log_level = None
    usage = 'geartype_rbt_runner.py --env <local | dev | prod> --log_level <info | debug | warning | error>'

    try:
        opts, args = getopt.getopt(argv, "h", ["env=", "log_level="])
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
    logger = log_utils.init_root_logger(logger_name="gearstack_rbt",
                                        log_path='../log/geartype_rbt.log',
                                        log_level=log_level)
    logger.info('Gearstack Gear Type Bot')
    logger.info('Environment: {0}'.format(env.upper()))
    logger.info('Log Level: {0}'.format(log_level.upper()))

    # Fetch configuration data for specified environment
    bot_configs = config_utils.fetch_bot_config(env)
    types = config_utils.fetch_data_config('cat_data_keys')

    # Instantiate retriever object
    type_retriever = GearTypeRetriever(amazon_config=bot_configs['amazon_config'],
                                       bot_db_configs=bot_configs['db_config']['bot_db_props'],
                                       app_db_configs=bot_configs['db_config']['app_db_props'])

    # Iterate through types list and persist
    try:
        for type in types:
            nodes_for_type = config_utils.fetch_data_config(config_name=type)
            type_retriever.save_geartypes(node_ids=nodes_for_type)
        logger.info('Finished persisting gear types!')
    except Exception:
        logger.exception('An error occurred during persistence of gear types!')
    finally:
        log_utils.close_logger(logger)


if __name__ == '__main__':
    main(sys.argv[1:])
