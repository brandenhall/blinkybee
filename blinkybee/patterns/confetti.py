import colorsys

from tornado.ioloop import PeriodicCallback
from random import randint
from blinkybee import settings, utils

class Pattern():
    def __init__(self, bee, info):
        self.bee = bee
        self.colors = [
            utils.hex_to_rgb(info.get('settings')[0].get('default')),
            utils.hex_to_rgb(info.get('settings')[1].get('default')),
            utils.hex_to_rgb(info.get('settings')[2].get('default'))]
        self.rate = int(info.get('settings')[3].get('default'))
        self.pixels = [(0,0,0)] * settings.PIXEL_COUNT
    
    def start(self):
        self.loop = PeriodicCallback(self.draw, 15)
        self.loop.start()
        self.draw()

    def stop(self):
        self.loop.stop()

    def update(self, options):
        if 'color_1' in options:
            self.colors[0] = utils.hex_to_rgb(options.get('color_1'))

        if 'color_2' in options:
            self.colors[1] = utils.hex_to_rgb(options.get('color_2'))

        if 'color_3' in options:
            self.colors[2] = utils.hex_to_rgb(options.get('color_3'))

        if 'rate' in options:
            self.rate = int(options.get('rate'))

    def draw(self):
        if randint(0, 100) <= self.rate:
            color = self.colors[randint(0,2)]
            self.pixels[randint(0, settings.PIXEL_COUNT - 1)] = color

        for idx, pixel in enumerate(self.pixels):
            if pixel != (0, 0, 0):
                h, s, v = colorsys.rgb_to_hsv(*utils.rgb_to_float(pixel))
                v -= 0.02
                if v <= 0:
                    self.pixels[idx] = (0, 0, 0)
                else:
                    self.pixels[idx] = utils.float_to_rgb(colorsys.hsv_to_rgb(h, s, v))

        self.bee.draw(self.pixels)