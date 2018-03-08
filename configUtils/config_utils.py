# ------------------------------------------------------------------------
#
# Module: config_utils.py
# Created By: coreym
# Created On: 2018/Feb/10
#
# Description: Defines static utility functions for retrieving
#              configuration properties from config files.
#
# ------------------------------------------------------------------------

import yaml
import os
from custom_errs.invalid_env_err import InvalidEnvException

""" Fetch config props from argument yaml config file. """
def fetch_bot_config(env='local'):
    if env.lower() == 'local' or env.lower() == 'dev' or env.lower() == 'prod':
        # Load yml config file into yaml reader
        config_file_path = os.path.join(os.path.dirname(__file__), '../config/bot_config.yml')
        with open(config_file_path, 'r') as yaml_file:
            cfg = yaml.load(yaml_file)

        # Return a dict of config props
        return {
            'db_config': {
                'app_db_props': {
                    'db_host': cfg[env]['app_db_props']['host'],
                    'db_name': cfg[env]['app_db_props']['db'],
                    'db_user': cfg[env]['app_db_props']['user'],
                    'db_pass': cfg[env]['app_db_props']['pass'],
                    'port': cfg[env]['app_db_props']['port']
                },
                'bot_log_db_props': {
                    'db_host': cfg[env]['bot_log_db_props']['host'],
                    'db_name': cfg[env]['bot_log_db_props']['db'],
                    'db_user': cfg[env]['bot_log_db_props']['user'],
                    'db_pass': cfg[env]['bot_log_db_props']['pass'],
                    'port': cfg[env]['bot_log_db_props']['port']
                },
                'bot_db_props': {
                    'db_host': cfg[env]['bot_db_props']['host'],
                    'db_name': cfg[env]['bot_db_props']['db'],
                    'db_user': cfg[env]['bot_db_props']['user'],
                    'db_pass': cfg[env]['bot_db_props']['pass'],
                    'port': cfg[env]['bot_db_props']['port']
                }
            },
            'amazon_config': {
                'api_access_key': cfg[env]['amazon_props']['access_key'],
                'api_secret_key': cfg[env]['amazon_props']['secret_key'],
                'associate_tag': cfg[env]['amazon_props']['associate_tag'],
                'cat_starter_node': cfg[env]['amazon_props']['cat_starter_node']
            }
        }
    else:
        raise InvalidEnvException('Invalid environment was specified: {0}'.format(env))

""" Fetch category nodes from cat_data.yml for argument category name. """
def fetch_cat_nodes(cat_name):
    # Load cat_data.yml into yml reader
    data_config_file_path = os.path.join(os.path.dirname(__file__), '../config/cat_data.yml')
    with open(data_config_file_path, 'r') as yaml_file:
        data_cfg = yaml.load(yaml_file)

    nodes = data_cfg[cat_name]
    return nodes

""" Fetch category key names from cat_data.yml. """
def fetch_cat_keys():
    # Load cat_data.yml into yml reader
    data_config_file_path = os.path.join(os.path.dirname(__file__), '../config/cat_data.yml')
    with open(data_config_file_path, 'r') as yaml_file:
        data_cfg = yaml.load(yaml_file)

    keys = data_cfg['cat_data_keys']
    return keys
