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
    def __init__(self):
        self.url = "https://api.openweathermap.org/data/2.5/onecall"

    def get_temperature(self, input_payload):
        payload = {
            "lang": "ja",
            "units": "metric",
            "appid": OWM_API_KEY,
        }
        payload.update(input_payload)
        response = requests.get(self.url, params=payload).json()

        return str(response["current"]["temp"])
