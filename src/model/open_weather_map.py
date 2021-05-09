#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import sys
import os

import requests

env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(env_path)
from env import OWM_API_KEY


class OpenWeatherMap:
    def __init__(self, input_payload):
        url = "https://api.openweathermap.org/data/2.5/onecall/timemachine"

        now = str(int(time.time()))
        payload = {
            "dt": now,
            "units": "metric",
            "appid": OWM_API_KEY,
        }
        payload.update(input_payload)

        self.response = requests.get(url, params=payload).json()
