# ------------------------------------------------------------------------
#
# Module: categories_retrieved_dao.py
# Created By: coreym
# Created On: 2018/Feb/24
#
# Description: Data access class for categories retrieved models.
#              Categories retrieved are stored in bot database.
#
# ------------------------------------------------------------------------

import logging
import dbUtils.db_utils as db_utils
import logUtils.log_utils as log_utils
from models.categories_retrieved import CategoryRetrieved


class CategoriesRetrievedDAO:
    def __init__(self, bot_db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(CategoriesRetrievedDAO.__name__))
        self.db_conn = db_utils.open_db_connection(bot_db_configs)

    def __del__(self):
        db_utils.close_db_connection(self.db_conn)

    """ Fetch category retrieved from category_retrieved table in bot db using name. """
    def fetch_category_by_name(self, name):
        try:
            sql = "SELECT * FROM categories_retrieved WHERE cat_name = %s"
            self.logger.debug('Executing SQL: {0}'.format(sql))
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [name])
                row = cursor.fetchone()
            if row:
                # Create CategoryRetrieved instance from fetched row values
                category = CategoryRetrieved(amazon_node_id=row[0],
                                             name=row[1],
                                             parent_node_id=row[2],
                                             is_leaf_node=row[3])
                return category
            else:
                return None
        except db_utils.psycopg2.DatabaseError as db_err:
            self.logger.exception('An error occurred during fetch operation on categories_retrieved table!')
            log_utils.close_logger(self.logger)
            raise db_err

    """ Fetch category from category table in bot database using argument node id. """
    def fetch_category_by_id(self, id):
        try:
            sql = "SELECT * FROM categories_retrieved WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [id])
                row = cursor.fetchone()
            if row:
                # Create Category instance from fetched row values
                category = CategoryRetrieved(amazon_node_id=row[0],
                                             name=row[1],
                                             parent_node_id=row[2],
                                             is_leaf_node=row[3])
                return category
            else:
                return None
        except db_utils.psycopg2.DatabaseError as db_err:
            self.logger.exception('An error occurred during fetch operation on categories_retrieved table!')
            log_utils.close_logger(self.logger)
            raise db_err

    """ Insert argument category_retrieved instance into database. """
    def insert_category(self, category_retrieved):
        try:
            ret_id = None
            sql = "INSERT INTO categories_retrieved " \
                  "(amazon_node_id, cat_name, parent_node_id, is_leaf_node) " \
                  "VALUES (%s, %s, %s, %s) RETURNING amazon_node_id;"

            self.logger.debug('Executing SQL: {0}'.format(sql))
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, (category_retrieved.amazon_node_id,
                                     category_retrieved.name,
                                     category_retrieved.parent_node_id,
                                     category_retrieved.is_leaf_node))
                ret_id = cursor.fetchone()[0]
                self.db_conn.commit()
            return ret_id
        except db_utils.psycopg2.DatabaseError as db_err:
            self.logger.exception('An error occurred during insert operation on categories_retrieved table!')
            log_utils.close_logger(self.logger)
            raise db_err

    """ Delete category_retrieved instance from database using argument node_id. """
    def delete_category(self, node_id):
        try:
            sql = "DELETE FROM categories_retrieved WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [node_id])
                self.db_conn.commit()
        except db_utils.psycopg2.DatabaseError as db_err:
            self.logger.exception('An error occurred during delete operation on categories_retrieved table!')
            log_utils.close_logger(self.logger)
            raise db_err
