# Copyright (C) 2016 Sahil Sareen (ssareen [AT] gnome [DOT] org)
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version. See http://www.gnu.org/copyleft/gpl.html the full text of the
# license.

import logging
import plotly.plotly as py


class PieChartPlotter:
    def __init__(self, labels, values, username, api_key, plot_name):
        self.logger = logging.getLogger(self.__class__.__name__)
        py.sign_in(username, api_key)
        fig = {
            'data': [{'labels': labels,
                      'values': values,
                      'type': 'pie'}],
            'layout': {'title': "Valentines week - %s #LoveIsInTheAir" % plot_name}
        }
        url = py.plot(fig, filename="Pie Chart %s" % plot_name)
        self.logger.info("Plotted Pie Chart: %s" % url)