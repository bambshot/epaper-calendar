#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys

from PIL import Image, ImageDraw, ImageFont


def get_dirpath_project_root(name):
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
        name,
    )


lib_dir = get_dirpath_project_root("lib")
sys.path.append(lib_dir)
from waveshare_epd.epd7in5_V2 import EPD


class EpaperRenderer:
    def __init__(self):
        self.epd = EPD()

    def template(self, data):
        assets_dir = get_dirpath_project_root("assets")
        font24 = ImageFont.truetype(os.path.join(assets_dir, "Font.ttc"), 24)

        image = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(image)

        draw.text((10, 0), "hello world", font=font24, fill=0)
        draw.text((10, 20), f'temperature: {data["temp"]}', font=font24, fill=0)
        draw.text((150, 0), "微雪电子", font=font24, fill=0)
        draw.line((20, 50, 70, 100), fill=0)
        draw.line((70, 50, 20, 100), fill=0)
        draw.rectangle((20, 50, 70, 100), outline=0)
        draw.line((165, 50, 165, 100), fill=0)
        draw.line((140, 75, 190, 75), fill=0)
        draw.arc((140, 50, 190, 100), 0, 360, fill=0)
        draw.rectangle((80, 50, 130, 100), fill=0)
        draw.chord((200, 50, 250, 100), 0, 360, fill=0)

        return image

    def render(self, data):
        self.epd.init()
        self.epd.Clear()
        image = self.template(data)
        self.epd.display(self.epd.getbuffer(image))
        self.epd.sleep()
