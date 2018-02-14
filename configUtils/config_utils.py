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
from custom_errs.invalid_env_err import InvalidEnvException

""" Fetch config props from argument yaml config file. """
def fetch_config(config_file_path, env='local'):
    if env.lower() == 'local' or env.lower() == 'dev' or env.lower() == 'prod':
        # Load yaml file into yaml reader
        with open(config_file_path, 'r') as yaml_file:
            cfg = yaml.load(yaml_file)

        # Return a dict of config props
        return {
            'app_db_props': {
                'db_host': cfg['local']['app_db_props']['host'],
                'db_name': cfg['local']['app_db_props']['db'],
                'db_user': cfg['local']['app_db_props']['user'],
                'db_pass': cfg['local']['app_db_props']['pass'],
                'port': cfg['local']['app_db_props']['port']
            },
            'log_db_props': {
                'db_host': cfg['local']['log_db_props']['host'],
                'db_name': cfg['local']['log_db_props']['db'],
                'db_user': cfg['local']['log_db_props']['user'],
                'db_pass': cfg['local']['log_db_props']['pass'],
                'port': cfg['local']['log_db_props']['port']
            }
        }
    else:
        raise InvalidEnvException('Invalid environment was specified: {0}'.format(env))


