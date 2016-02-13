# Copyright (C) 2016 Sahil Sareen (ssareen [AT] gnome [DOT] org)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version. See http://www.gnu.org/copyleft/gpl.html the full text of the
# license.

# 1. Reads the tuples from the partition files created by the twitter spark streaming
#    application <Tuples are of the form (CITY_NAME,NUM_TWEETS)>
# 2. Each CITY_NAME is mapped to an Indian State using geopy
#    and the tweet count is accumulated for each state
# 3. A pie chart is plotted using PieChartPlotter for ease of visualizing the results

# To improve the performance(speed) a cache of cities is maintained and appended to on every run
# This is because the twitter stream app is appending to the already found cities continuously


import logging
from geopy.geocoders import Nominatim

from CacheAppender import CacheAppender
from CachedCities import cached_cities
from ConfigReader import ConfigReader
from PieChartPlotter import PieChartPlotter
from States import states_in_india
from UnionTerritories import union_territories
from UnmatchedCities import unmatched_cities

DEFAULT_CONFIG_FILE = "../resources/config.json"


class StatesTweetCount:
    def __init__(self, config_file=DEFAULT_CONFIG_FILE):
        self.config = ConfigReader(config_file)
        self.states = {}
        self.geo_locator = Nominatim()
        self.tweet_count = 0
        self.city_cache_appender = CacheAppender(self.config.cache_file_path)

        def get_level():
            return {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARN': logging.WARNING,
                'ERROR': logging.ERROR,
                'FATAL': logging.FATAL,
                'CRITICAL': logging.CRITICAL
            }[self.config.logging_level]

        logging.basicConfig(format="[%(levelname)s] %(name)s: %(message)s", level=get_level())

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Analysing city names using config in %s" % config_file)

    def increment_tweet_count(self, state_name, count):
        self.tweet_count += count
        if state_name in self.states.keys():
            self.states[state_name] += count
        else:
            self.states[state_name] = count

    def get_full_address(self, city_name):
        # Append "India" to CITY_NAME for accurate results
        location = self.geo_locator.geocode("%s India" % city_name,
                                            timeout=self.config.geopy_timeout)
        if location is None:
            return unmatched_cities[city_name]
        return location.address

    def search_states(self, address):
        for state in states_in_india:
            if state in address:
                return state
        return None

    def search_union_territories(self, address):
        for union_ter in union_territories:
            if union_ter in address:
                return union_ter
        return None

    def process_address_tweet(self, address):
        state_check = self.search_states(address)
        if state_check is not None:
            return state_check
        else:
            union_ter = self.search_union_territories(address)
            if union_ter is not None:
                return union_ter
        self.logger.error("[GEOPY] Address not found: %s" % address)
        return None

    def append_to_cache(self, city, state):
        if self.config.update_cache_file:
            self.city_cache_appender.append_cached_data(city, state)

    def read_tweet_cities(self, file_name):
        tuples = []
        for part in xrange(0, self.config.spark_num_partitions):
            spark_file = open(self.config.spark_file_name % part)
            try:
                tuples += spark_file.readlines()
            finally:
                spark_file.close()

        self.logger.info("Processing cities: %s" % tuples)
        for city_tuple in tuples:
            self.logger.debug("Processing city tuple: %s" % city_tuple.rstrip())
            city_name, tweet_count = city_tuple[1:].strip("(|)\n").split(",")
            if city_name in cached_cities.keys():
                state = cached_cities[city_name]
                self.logger.debug("Mapped city: %s to state: %s" % (city_name, state))
                self.increment_tweet_count(state, int(tweet_count))
            else:
                address = self.get_full_address(city_name)
                state = self.process_address_tweet(address)
                self.logger.debug("Mapped city: %s to state: %s" % (city_name, state))
                self.increment_tweet_count(state, int(tweet_count))
                self.append_to_cache(city_name, state)

    def run(self):
        try:
            self.read_tweet_cities(self.config.spark_file_name)
            if self.logger.isEnabledFor(logging.INFO):
                for state, num_tweets in self.states.iteritems():
                    self.logger.info("[%s] Tweets: %s, Percentage: %s" % (
                        state,
                        num_tweets,
                        (num_tweets * 100.0) / self.tweet_count))

            PieChartPlotter(self.states.keys(),
                            self.states.values(),
                            self.config.plotly_username,
                            self.config.plotly_api_key,
                            self.config.plotly_plot_name)
        finally:
            if self.config.update_cache_file:
                self.city_cache_appender.append_cache_file()

if __name__ == '__main__':
    StatesTweetCount().run()
