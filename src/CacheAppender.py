# Copyright (C) 2016 Sahil Sareen (ssareen [AT] gnome [DOT] org)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version. See http://www.gnu.org/copyleft/gpl.html the full text of the
# license.

# Append new cities found using GeoPy to the CachedCities
# to be able to do a faster lookup in future

import logging


class CacheAppender:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cached_data = ""
        self.logger = logging.getLogger(self.__class__.__name__)

    def append_cached_data(self, city, state):
        self.logger.debug("Appending city: '%s' to CachedCities.py" % city)
        self.cached_data += "cached_cities[\"%s\"] = \"%s\"\n" % (city, state)

    def append_cache_file(self):
        with open(self.file_name, "a") as cached_cities_file:
            cached_cities_file.write(self.cached_data)
