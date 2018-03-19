# ------------------------------------------------------------------------
#
# Module: gear_dao.py
# Created By: coreym
# Created On: 2018/Mar/09
#
# Description:  Provides data access functions for persisting gear data
#               to application database.
#
# ------------------------------------------------------------------------

import logging
import dbUtils.db_utils as db_utils
import logUtils.log_utils as log_utils
from models.gear import Gear


class GearDAO:
    def __init__(self, app_db_config):
        self.logger = logging.getLogger('gear_rbt_logger.{0}'.format(GearDAO.__name__))
        self.db_conn = db_utils.open_db_connection(db_configs=app_db_config)

    def __del__(self):
        db_utils.close_db_connection(self.db_conn)


    """ Saves a new gear record to gear table in app database. """
    def save_gear(self, gear):
        try:
            sql = "INSERT INTO gear (name, description, thumb_url, amazon_link, " \
                  "image_url, manufacturer, type_id, features) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, (gear.name,
                                     gear.description,
                                     gear.thumb_url,
                                     gear.amazon_link,
                                     gear.image_url,
                                     gear.manufacturer,
                                     gear.type_id,
                                     gear.features))
                rec = cursor.fetchone()
                if rec:
                    self.db_conn.commit()
                    return rec[0]
                else:
                    return None
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during save operation on gear table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err


    """ Deletes existing gear record from gear table in app database. """
    def delete_gear(self, gear_id):
        try:
            sql = "DELETE FROM gear WHERE id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [gear_id])
                self.db_conn.commit()
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during delete operation on gear table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err


    """ Fetches gear record from gear table using argument gear_id. """
    def fetch_gear_by_id(self, gear_id):
        try:
            sql = "SELECT * from gear WHERE id = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [gear_id])
                record = cursor.fetchone()

                if record:
                    gear = Gear(name=record[1],
                                description=record[2],
                                thumb_url=record[3],
                                amazon_link=record[4],
                                image_url=record[5],
                                manufacturer=record[6],
                                type_id=record[7],
                                features=record[8])
                    return gear
                else:
                    return None
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during fetch by id operation on gear table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err


    """ Fetches gear record from gear table using argument gear_name. """
    def fetch_gear_by_name(self, gear_name):
        try:
            sql = "SELECT * from gear WHERE name = %s;"
            self.logger.debug('Executing SQL: {0}'.format(sql))

            with self.db_conn.cursor() as cursor:
                cursor.execute(sql, [gear_name])
                record = cursor.fetchone()

                if record:
                    gear = Gear(name=record[1],
                                description=record[2],
                                thumb_url=record[3],
                                amazon_link=record[4],
                                image_url=record[5],
                                manufacturer=record[6],
                                type_id=record[7],
                                features=record[8])
                    return gear
                else:
                    return None
        except (db_utils.psycopg2.DatabaseError, Exception) as err:
            self.logger.exception('An error occurred during fetch by name operation on gear table!')
            log_utils.close_logger(self.logger)
            db_utils.close_db_connection(self.db_conn)
            raise err
