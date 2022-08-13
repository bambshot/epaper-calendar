#!/usr/bin/python
# -*- coding:utf-8 -*-
from datetime import datetime
import locale
import logging

from google.auth import load_credentials_from_file
from env import GOOGLE_CALENDAR_ID, OWM_API_KEY
from model.google_calendar import GoogleCalendar
from model.open_weather_map import OpenWeatherMap
from view.epaper_renderer import EpaperRenderer


def main():
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

    now = datetime.now()
    date_str = now.strftime("%Y.%m.%d")
    day_of_week_str = now.strftime("%a")

    weather = OpenWeatherMap(OWM_API_KEY)
    daily_forcast = weather.get_daily_forecast({"lat": "35.71", "lon": "139.81"})

    scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
    cred = load_credentials_from_file("service-account.json", scopes)[0]
    calendar = GoogleCalendar(cred)
    events = []
    for event in calendar.get_events(calendar_id=GOOGLE_CALENDAR_ID, max_results=5):
        events.append(
            {
                "period": event["period"],
                "summary": event["summary"],
            }
        )

    renderer = EpaperRenderer()
    renderer.render(
        {
            "date": date_str,
            "day_of_week": day_of_week_str,
            "forecasts": [daily_forcast[0], daily_forcast[1]],
            "events": events,
        }
    )


try:
    main()

except IOError as e:
    logging.info(e)
