#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import logging
import time

from PIL import Image, ImageDraw, ImageFont

libdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "lib"
)
sys.path.append(libdir)
from waveshare_epd import epd7in5_V2

picdir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "assets"
)

logging.basicConfig(level=logging.DEBUG)


class Controller:
    def __init__(self):
        self.setup()
        self.main()
        self.teardown()

    def setup(self):
        logging.info("init and Clear")
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
        self.epd.Clear()

    def main(self):
        # view
        font24 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, "Font.ttc"), 18)

        # Drawing on the Horizontal image
        logging.info("1.Drawing on the Horizontal image...")
        # 255: clear the frame
        Himage = Image.new("1", (self.epd.width, self.epd.height), 255)
        draw = ImageDraw.Draw(Himage)
        draw.text((10, 0), "hello world", font=font24, fill=0)
        draw.text((10, 20), "7.5inch e-Paper", font=font24, fill=0)
        draw.text((150, 0), u"微雪电子", font=font24, fill=0)
        draw.line((20, 50, 70, 100), fill=0)
        draw.line((70, 50, 20, 100), fill=0)
        draw.rectangle((20, 50, 70, 100), outline=0)
        draw.line((165, 50, 165, 100), fill=0)
        draw.line((140, 75, 190, 75), fill=0)
        draw.arc((140, 50, 190, 100), 0, 360, fill=0)
        draw.rectangle((80, 50, 130, 100), fill=0)
        draw.chord((200, 50, 250, 100), 0, 360, fill=0)
        self.epd.display(self.epd.getbuffer(Himage))
        time.sleep(2)

        # Drawing on the Vertical image
        logging.info("2.Drawing on the Vertical image...")
        Limage = Image.new("1", (self.epd.height, self.epd.width), 255)
        draw = ImageDraw.Draw(Limage)
        draw.text((2, 0), "hello world", font=font18, fill=0)
        draw.text((2, 20), "7.5inch epd", font=font18, fill=0)
        draw.text((20, 50), u"微雪电子", font=font18, fill=0)
        draw.line((10, 90, 60, 140), fill=0)
        draw.line((60, 90, 10, 140), fill=0)
        draw.rectangle((10, 90, 60, 140), outline=0)
        draw.line((95, 90, 95, 140), fill=0)
        draw.line((70, 115, 120, 115), fill=0)
        draw.arc((70, 90, 120, 140), 0, 360, fill=0)
        draw.rectangle((10, 150, 60, 200), fill=0)
        draw.chord((70, 150, 120, 200), 0, 360, fill=0)
        self.epd.display(self.epd.getbuffer(Limage))
        time.sleep(2)

        logging.info("3.read bmp file")
        Himage = Image.open(os.path.join(picdir, "7in5_V2.bmp"))
        self.epd.display(self.epd.getbuffer(Himage))
        time.sleep(2)

        logging.info("4.read bmp file on window")
        # 255: clear the frame
        Himage2 = Image.new("1", (self.epd.height, self.epd.width), 255)
        bmp = Image.open(os.path.join(picdir, "100x100.bmp"))
        Himage2.paste(bmp, (50, 10))
        self.epd.display(self.epd.getbuffer(Himage2))
        time.sleep(2)

    def teardown(self):
        logging.info("Goto Sleep...")
        self.epd.sleep()


try:
    Controller()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd7in5_V2.epdconfig.module_exit()
    exit()
