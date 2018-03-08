# ------------------------------------------------------------------------
#
# Module: gear_type_retrieved.py
# Created By: coreym
# Created On: 2018/Mar/07
#
# Description: Model for gear_type_retrieved table object of bot database.
#              Records are saved to this table so I don't have to search
#              the application database to check for existence before
#              insert.
#
# ------------------------------------------------------------------------

class GearTypeRetrieved:
    def __init__(self, amazon_node_id):
        self.amazon_node_id = amazon_node_id

    def __str__(self):
        return "Gear Type:\nNode Id: {0}".format(self.amazon_node_id)
