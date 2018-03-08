# ------------------------------------------------------------------------
#
# Module: geartype_retriever.py
# Created By: coreym
# Created On: 2018/Feb/18
#
# Description: Uses Amazon PAAPI to retrieve musical instrument categories
#              and saves them to the bot database categories table.
#
# ------------------------------------------------------------------------

import logging
import urllib2
import threading
from amazon.api import AmazonAPI

import configUtils.config_utils as config_utils
from dao.geartype_retrieved_dao import GearTypeRetrievedDAO
from dao.geartype_dao import GearTypeDAO
from models.gear_type_retrieved import GearTypeRetrieved
from models.gear_type import GearType


class GearTypeRetriever:
    """ Initialize retriever class with Amazon access configs. """
    def __init__(self, amazon_config, bot_db_configs, app_db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(GearTypeRetriever.__name__))
        self.amazon_config = amazon_config
        self.geartype_retrieved_dao = GearTypeRetrievedDAO(bot_db_configs=bot_db_configs)
        self.geartype_dao = GearTypeDAO(app_db_configs=app_db_configs)
        self.amazon = AmazonAPI(aws_key=amazon_config['api_access_key'],
                                aws_secret=amazon_config['api_secret_key'],
                                aws_associate_tag=amazon_config['associate_tag'])
        self.cats_to_ignore = config_utils.fetch_cat_nodes('ignore_cats')


    """ Uses Amazon PAAPI to perform a node lookup. """
    def node_lookup(self, node_id, retry_cnt=0):
        # Initialize amazon api instance to use
        self.logger.debug('Performing node lookup for node id {0}'.format(node_id))
        try:
            result = self.amazon.browse_node_lookup(ResponseGroup="BrowseNodeInfo", BrowseNodeId=node_id)
            return result[0]
        except IndexError:
            return None
        except urllib2.HTTPError as http_err:
            if http_err.code == 503:
                # This exception indicates that I might be exceeding Amazon's request limit.
                # Need to execute some re-try logic here.
                if (retry_cnt < 5):
                    # Try one second retry a few times
                    self.logger.warning('Request limit. Amazon is throttling requests. '
                                        'Retry count: {0}'.format(retry_cnt))
                    threading.Timer(1.0, self.node_lookup(node_id=node_id, retry_cnt=retry_cnt + 1))
                elif (retry_cnt >=5 and retry_cnt < 10):
                    # If one second retries don't work, try 10 second retries a few times
                    self.logger.warning('Request limit. Amazon is throttling requests. '
                                        'Retry count: {0}'.format(retry_cnt))
                    threading.Timer(10.0, self.node_lookup(node_id, retry_cnt + 1))
                else:
                    # If none of previous retries work, stop trying and raise error
                    self.logger.exception('Maximum retry count reached while attempting to lookup category!')
                    raise http_err
            else:
                self.logger.exception('Unexpected HTTP error encountered during category lookup!')
                raise http_err

    """ Performs node lookup for each node in arg nodes. Then saves
        node and its ancestors to the database. Node_ids comes from
        the list of node_ids in cat_data.yml config file. Function also
        saves GearType instances to gear_type table in gearstack app
        database if they don't already exist in gear_type_retrieved
        table in bot_database. Bot database tables exist so that app
        database tables don't need to be searched to determine if a 
        gear type already exists. """
    def save_geartypes(self, node_ids):
        for node_id in node_ids:
            if not self.geartype_retrieved_dao.fetch_geartype_retrieved_by_id(node_id=node_id):
                # Lookup node
                node = self.node_lookup(node_id)

                if node:
                    # Add current node and all ancestors to nodes_to_persist
                    nodes_to_persist = []
                    nodes_to_persist.append(node)
                    nodes_to_persist.extend(node.ancestors)

                    # Reverse nodes_to_persist list to start with root node
                    nodes_to_persist.reverse()
                    for n in nodes_to_persist:
                        if n.id not in self.cats_to_ignore:
                            if not self.geartype_retrieved_dao.fetch_geartype_retrieved_by_id(node_id=n.id):
                                # First save GearType to app database
                                gear_type = GearType(amazon_node_id=n.id,
                                                     name=str(n.name),
                                                     parent_node_id=n.ancestor.id if n.ancestor and
                                                                     n.ancestor.id not in self.cats_to_ignore else None,
                                                     is_leaf_node=True if n.id == node.id else False)
                                ret_type_id = self.geartype_dao.insert_geartype(gear_type=gear_type)

                                if ret_type_id is not None:
                                    # Log success
                                    self.logger.debug('Saved gear type: {0} with id {1} to db!'.format(gear_type.name,
                                                                                                       ret_type_id))

                                    # Now save GearTypeRetrieved instance to bot database if GearType save
                                    # was successful
                                    gear_type_retrieved = GearTypeRetrieved(amazon_node_id=n.id)
                                    self.geartype_retrieved_dao.insert_geartype_retrieved(
                                        gear_type_retrieved=gear_type_retrieved)
                                    self.logger.debug('Saved node {0} to db!'.format(str(n.id)))
                                else:
                                    # Log gear type save failure
                                    self.logger.debug('Save unsuccessful for '
                                                      'gear type {0} with id {1}!'.format(gear_type.name,
                                                                                          gear_type.amazon_node_id))
                else:
                    self.logger.warning('Could not find node {0} via look up!'.format(node_id))
