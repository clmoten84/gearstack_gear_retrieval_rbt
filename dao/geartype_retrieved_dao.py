# ------------------------------------------------------------------------
#
# Module: geartype_retrieved_dao.py
# Created By: coreym
# Created On: 2018/Feb/24
#
# Description: Data access class for GearTypeRetrieved models.
#              GearTypeRetrieved objects are stored in bot database.
#
# ------------------------------------------------------------------------

import logging
import dbUtils.db_utils as db_utils
import logUtils.log_utils as log_utils
from models.gear_type_retrieved import GearTypeRetrieved


class GearTypeRetrievedDAO:
    def __init__(self, bot_db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(GearTypeRetrievedDAO.__name__))
        self.db_conn = db_utils.open_db_connection(bot_db_configs)

    def __del__(self):
        db_utils.close_db_connection(self.db_conn)

    """ Fetch category from category table in bot database using argument node id. """
    def fetch_geartype_retrieved_by_id(self, node_id):
        try:
            sql = "SELECT * FROM gear_type_retrieved WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [node_id])
                row = cursor.fetchone()
            if row:
                # Create GearTypeRetrieved instance from fetched row values
                gear_type_retrieved = GearTypeRetrieved(amazon_node_id=row[0])
                return gear_type_retrieved
            else:
                return None
        except (db_utils.psycopg2.DatabaseError, Exception) as db_err:
            self.logger.exception('An error occurred during fetch operation on gear_type_retrieved table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise db_err

    """ Insert argument category_retrieved instance into database. """
    def insert_geartype_retrieved(self, gear_type_retrieved):
        try:
            ret_id = None
            sql = "INSERT INTO gear_type_retrieved " \
                  "(amazon_node_id) " \
                  "VALUES (%s) RETURNING amazon_node_id;"

            self.logger.debug('Executing SQL: {0}'.format(sql))
            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [gear_type_retrieved.amazon_node_id])
                ret_id = cursor.fetchone()[0]
                self.db_conn.commit()
            return ret_id
        except (db_utils.psycopg2.DatabaseError, Exception) as db_err:
            self.logger.exception('An error occurred during insert operation on gear_type_retrieved table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise db_err

    """ Delete category_retrieved instance from database using argument node_id. """
    def delete_geartype_retrieved(self, node_id):
        try:
            sql = "DELETE FROM gear_type_retrieved WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [node_id])
                self.db_conn.commit()
        except (db_utils.psycopg2.DatabaseError, Exception) as db_err:
            self.logger.exception('An error occurred during delete operation on gear_type_retrieved table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise db_err
