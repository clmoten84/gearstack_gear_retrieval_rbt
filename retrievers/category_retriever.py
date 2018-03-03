# ------------------------------------------------------------------------
#
# Module: category_retriever.py
# Created By: coreym
# Created On: 2018/Feb/18
#
# Description: Uses Amazon PAAPI to retrieve musical instrument categories
#              and saves them to the bot database categories table.
#
# ------------------------------------------------------------------------

import logging
from amazon.api import AmazonAPI

from dao.categories_retrieved_dao import CategoriesRetrievedDAO
from models.categories_retrieved import CategoryRetrieved


class CategoryRetriever:
    """ Initialize retriever class with Amazon access configs. """
    def __init__(self, amazon_config, bot_db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(CategoryRetriever.__name__))
        self.amazon_config = amazon_config
        self.dao = CategoriesRetrievedDAO(bot_db_configs=bot_db_configs)


    """ Uses Amazon PAAPI to perform a node lookup. """
    def node_lookup(self, node_id):
        # Initialize amazon api instance to use
        self.logger.debug('Performing node lookup for node id {0}'.format(node_id))
        amazon = AmazonAPI(aws_key=self.amazon_config['api_access_key'],
                           aws_secret=self.amazon_config['api_secret_key'],
                           aws_associate_tag=self.amazon_config['associate_tag'])
        result = amazon.browse_node_lookup(ResponseGroup="BrowseNodeInfo", BrowseNodeId=node_id)
        try:
            return result[0]
        except IndexError:
            return None

    """ Recursively persist argument node and its children to database. """
    def persist_categories(self, node_id, parent_node_id=None):
        # Lookup node
        node = self.node_lookup(node_id)

        if node:
            if not self.dao.fetch_category_by_id(id=node_id):
                # Category was not found in database - so persist it
                name = node.name
                children = node.children
                is_leaf_node = len(children) == 0
                category = CategoryRetrieved(amazon_node_id=node_id,
                                             name=name,
                                             parent_node_id=parent_node_id,
                                             is_leaf_node=is_leaf_node)
                self.dao.insert_category(category_retrieved=category)

                # Recurse for each child in children list
                for child in children:
                    self.persist_categories(node_id=child.id, parent_node_id=node_id)

    """ Execute retriver - this will run entire category retrieve operation. """
    def execute_retriever(self):
        # Start with starting node_id and process each child node in turn
        starter_node = self.node_lookup(node_id=self.amazon_config['cat_starter_node'])

        if starter_node:
            starter_children = starter_node.children
            for child in starter_children:
                self.persist_categories(child.id, parent_node_id=starter_node.id)
        else:
            self.logger.error('Starter node could not be found via look up! Check the node id'
                              ' for the starter node!')
            raise Exception('An error occurred during category_retriever execution!')
