# ------------------------------------------------------------------------
#
# Module: gear_retriever.py
# Created By: coreym
# Created On: 2018/Mar/09
#
# Description:  Uses Amazon PAAPI to retrieve music gear from Amazon
#               and saves the gear data to the application database.
#
# ------------------------------------------------------------------------

import logging
import time
import re
import urllib2
import amazon.api

from dao.gear_dao import GearDAO
from models.gear import Gear


class GearRetriever:
    def __init__(self, amazon_config, app_db_config, exclusion_keys):
        self.logger = logging.getLogger('gear_rbt_logger.{0}'.format(GearRetriever.__name__))
        self.amazon = amazon.api.AmazonAPI(aws_key=amazon_config['api_access_key'],
                                aws_secret=amazon_config['api_secret_key'],
                                aws_associate_tag=amazon_config['associate_tag'])
        self.exclusion_keys = exclusion_keys  # Should be list of keywords for item exclusion
        self.gear_dao = GearDAO(app_db_config)


    """ Use Amazon PAAPI to search for items in the argument browse node. 
        Excludes all items whose titles contain exclusion keywords (i.e. 
        kit, pack, etc. """
    def search_items(self, browse_node_id, price_limit=500000):
        fetched_products = []
        min_price = 100
        max_price = 5000

        # Loop and increment min_price and max_price by 50 until price_limit is reached
        while max_price <= price_limit:
            # Prevent API request throttling
            try:
                time.sleep(2.0)
                products = self.amazon_search(search_idx='MusicalInstruments',
                                              browse_node=browse_node_id,
                                              sort='-price',
                                              min_price=min_price,
                                              max_price=max_price)

                skip_cnt = 0  #Indicates how many items were skipped by exclusion
                for i, product in enumerate(products):
                    # Sanitize data by excluding products with relevant exclusion keys
                    skip = False
                    for keyword in self.exclusion_keys:
                        if keyword in product.title:
                            skip = True
                            skip_cnt = skip_cnt + 1
                            break

                    if not skip:
                        fetched_products.append(product)

                self.logger.debug("Request for items in node {0} ({1} - {2}) yielded {3} results."
                                  .format(browse_node_id, min_price, max_price, (i+1)-skip_cnt))
            except amazon.api.SearchException:
                self.logger.debug('No matches found for search request with args: [{0} - {1} - {2} - {3} - {4}]'
                                  .format('MusicalInstruments', browse_node_id, '-price', min_price, max_price))

            # Increment min and max price variables
            min_price = min_price + 5000
            max_price = max_price + 5000

        return fetched_products

    """ Executes Amazon PAAPI search request with arguments. If a 503 error is encountered,
        it indicates that the request was throttled. Retry logic is implemented in this case.
        If all retry attempts fail the exception is raised to caller for handling. """
    def amazon_search(self, search_idx, browse_node, sort, min_price, max_price, retry_cnt=0):
        try:
            items = self.amazon.search(SearchIndex=search_idx,
                                       BrowseNode=browse_node,
                                       Sort=sort,
                                       MinimumPrice=min_price,
                                       MaximumPrice=max_price)
            return items
        except urllib2.HTTPError as http_err:
            if http_err.code == 503:  #Indicates Amazon API request throttling - implement retry logic
                if retry_cnt < 6:  #Retry every 10 seconds for one minute before giving up
                    self.logger.debug("Amazon appears to be throttling requests. "
                                      "Retrying request... (Retry count = {0})".format(retry_cnt))
                    time.sleep(10.0)
                    self.amazon_search(search_idx=search_idx,
                                       browse_node=browse_node,
                                       sort=sort,
                                       min_price=min_price,
                                       max_price=max_price,
                                       retry_cnt=retry_cnt+1)
                else:
                    self.logger.debug("Max retry count reached while attempting Amazon API search request!")
                    raise http_err


    """ Persist argument item in item_list to application database. """
    def save_gear(self, item_list, browse_node):
        for item in item_list:
            name = item.title
            thumb_url = item.small_image_url
            manufacturer = item.brand
            type_id = browse_node
            amazon_link = item.detail_page_url
            image_url = item.large_image_url
            description = self.clean_html(item.editorial_review)

            features = ""
            for i, feature in enumerate(item.features):
                if i == 0:
                    features = "{0}".format(self.clean_html(feature))
                else:
                    features = "{0};{1}".format(features, self.clean_html(feature))

            # Create Gear instance and save to database
            gear = Gear(name=name,
                        description=description,
                        thumb_url=thumb_url,
                        amazon_link=amazon_link,
                        image_url=image_url,
                        manufacturer=manufacturer,
                        type_id=type_id,
                        features=features)

            ret_id = self.gear_dao.save_gear(gear)
            if ret_id is not None:
                # Log success
                self.logger.info("Saved gear {0} with id {1}".format(gear.name, ret_id))

    """ Cleans the argument string of all HTML tags """
    def clean_html(self, html_string):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', html_string)
        return str(cleantext)
