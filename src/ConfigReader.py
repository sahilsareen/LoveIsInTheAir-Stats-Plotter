# Copyright (C) 2016 Sahil Sareen (ssareen [AT] gnome [DOT] org)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version. See http://www.gnu.org/copyleft/gpl.html the full text of the
# license.

import json


class ConfigReader:
    def __init__(self, file_name):
        with open(file_name) as data_file:
            config = json.load(data_file)

        # Application Config
        self.logging_level = config["logging_level"]
        self.update_cache_file = config["update_cache_file"]
        self.cache_file_path = config["cache_file_path"]

        # Spark Config
        self.spark_file_name = config["spark_file_name"]
        self.spark_num_partitions = config["spark_num_partitions"]

        # Geopy Config
        self.geopy_timeout = config["geopy_timeout"]

        # Plotly Config
        self.plotly_username = config["plotly_username"]
        self.plotly_api_key = config["plotly_api_key"]
        self.plotly_plot_name = config["plotly_plot_name"]
