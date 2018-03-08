# ------------------------------------------------------------------------
#
# Module: geartype_dao.py
# Created By: coreym
# Created On: 2018/Mar/07
#
# Description:  Data access class for GearType models. GearType objects
#               are stored in gearstack application database.
#
# ------------------------------------------------------------------------

import logging
import dbUtils.db_utils as db_utils
import logUtils.log_utils as log_utils
from models.gear_type import GearType


class GearTypeDAO:
    def __init__(self, app_db_configs):
        self.logger = logging.getLogger('gearstack_rbt.{0}'.format(GearTypeDAO.__name__))
        self.db_conn = db_utils.open_db_connection(app_db_configs)

    def __del__(self):
        db_utils.close_db_connection(self.db_conn)

    """ Fetch GearType instance by type id. """
    def fetch_geartype_by_id(self, type_id):
        try:
            sql = "SELECT * FROM gear_type WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [type_id])
                row = cursor.fetchone()
            if row:
                gear_type = GearType(amazon_node_id=row[0],
                                     name=row[1],
                                     parent_node_id=row[2],
                                     is_leaf_node=row[3])
                return gear_type
            else:
                return None
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during fetch by id operation on gear_type table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err

    """ Fetch GearType instance by type name. """
    def fetch_geartype_by_name(self, name):
        try:
            sql = "SELECT * FROM gear_type WHERE cat_name = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [name])
                row = cursor.fetchone()
            if row:
                gear_type = GearType(amazon_node_id=row[0],
                                     name=row[1],
                                     parent_node_id=row[2],
                                     is_leaf_node=row[3])
                return gear_type
            else:
                return None
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during fetch by name operation on gear_type table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err

    """ Insert GearType instance to gear_type table of gearstack db. """
    def insert_geartype(self, gear_type):
        try:
            sql = "INSERT INTO gear_type " \
                  "(amazon_node_id, cat_name, parent_node_id, is_leaf_node) " \
                  "VALUES (%s, %s, %s, %s) RETURNING amazon_node_id;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, (gear_type.amazon_node_id,
                                     gear_type.name,
                                     gear_type.parent_node_id,
                                     gear_type.is_leaf_node))
                ret_id = cursor.fetchone()[0]
                self.db_conn.commit()
            return ret_id
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during insert operation on gear_type table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err

    """ Delete GearType instance from gear_type table of gearstack db. """
    def delete_geartype(self, type_id):
        try:
            sql = "DELETE FROM gear_type WHERE amazon_node_id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [type_id])
                self.db_conn.commit()
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during delete operation on gear_type table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err
