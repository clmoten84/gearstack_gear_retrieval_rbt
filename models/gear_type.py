# ------------------------------------------------------------------------
#
# Module: gear_type.py
# Created By: coreym
# Created On: 2018/Feb/24
#
# Description: Model for gear_type table object of gearstack database
#
# ------------------------------------------------------------------------

class GearType:
    def __init__(self, amazon_node_id, name, parent_node_id, is_leaf_node):
        self.amazon_node_id = amazon_node_id
        self.name = name
        self.parent_node_id = parent_node_id
        self.is_leaf_node = is_leaf_node

    def __str__(self):
        return "Gear Type:\nNode Id: {0}\n" \
               "Name: {1}\n" \
               "Parent Node: {2}\n" \
               "Leaf Node: {3}".format(self.amazon_node_id,
                                       self.name,
                                       self.parent_node_id,
                                       self.isleaf_node)

