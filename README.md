# LoveIsInTheAir-Stats-Plotter
A pie chart plotter for Spark twitter steaming data collected from all over India during the valentines week built using plotly and geopy. Plots the distribution of tweets for all the states of India.

# Tweets of love from India (Feb 7-14, 2016)

[<img src="http://i.imgur.com/q1ZV1Gt.png" />](https://plot.ly/~sahilsareen/10.embed)

- Click to see the pie chart on plot.ly

# Setup and HowTo

0. Install `python-2.7`

1. Install the following modules using `pip install`: `geopy`, `plotly`, `json`, `logging`

2. Clone LoveIsInTheAir-Stats-Plotter: `git clone https://github.com/sahilsareen/LoveIsInTheAir-Stats-Plotter.git`

3. Get a [`plot.ly`](https://plot.ly/) account

4. Update the [configuration](https://github.com/sahilsareen/LoveIsInTheAir-Stats-Plotter/blob/master/resources/config.json)
  - Set the spark config:
    - `spark_file_name`: The location where the spark streamed twitter cached files are stored by [LoveIsInTheAir](https://github.com/sahilsareen/LoveIsInTheAir)
    - `spark_num_partitions`: The number of cached files stored as [partitions](https://github.com/sahilsareen/LoveIsInTheAir-Stats-Plotter/tree/master/sample_spark_data)
  - `geopy_timeout`: Timeout per city to state lookup by geopy
  - Set the plotly config:
    - `plotly_username`: Your username on [`plot.ly`](https://plot.ly/)
    - `plotly_api_key`: Your [`api-key`](https://plot.ly/settings/api)
    - `plotly_plot_name`: Name of the pie chart

5. Run `cd LoveIsInTheAir-Stats-Plotter/src && python StatesTweetCount.py`

# Contributing

1. Generate a pull request, OR
2. Email patches to `sahil [DOT] sareen [AT] hotmail [DOT] com`

* Stick to the [python style guide](https://www.python.org/dev/peps/pep-0008/)

# License

See [Liscence](https://github.com/sahilsareen/LoveIsInTheAir-Stats-Plotter/blob/master/LICENSE)

# Author

- Sahil Sareen (sahil [DOT] sareen [AT] hotmail [DOT] com)
