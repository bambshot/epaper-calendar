#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

# from model.google_calendar import GoogleCalendar
from model.open_weather_map import OpenWeatherMap
from view.epaper_renderer import EpaperRenderer

logging.basicConfig(level=logging.DEBUG)


def main():
    # calendar = GoogleCalendar()
    weather = OpenWeatherMap()
    temperature = weather.get_temperature({"lat": "35.71", "lon": "139.81"})

    renderer = EpaperRenderer()
    data = {"temp": temperature}
    renderer.render(data)


try:
    main()

except IOError as e:
    logging.info(e)
