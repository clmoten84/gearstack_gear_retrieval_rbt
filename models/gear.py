# ------------------------------------------------------------------------
#
# Module: gear.py
# Created By: coreym
# Created On: 2018/Mar/09
#
# Description: Model representing a Gear instance
#
# ------------------------------------------------------------------------


class Gear:
    def __init__(self, name, description, thumb_url, amazon_link, image_url,
                 manufacturer, type_id, features):
        self.name = name
        self.description = description
        self.thumb_url = thumb_url
        self.amazon_link = amazon_link
        self.image_url = image_url
        self.manufacturer = manufacturer
        self.type_id = type_id
        self.features = features

    def __str__(self):
        return "Gear:\nName: {0}\n" \
               "Manufacturer: {1}\n" \
               "Type Id: {2}".format(self.name,
                                     self.manufacturer,
                                     self.type_id)
