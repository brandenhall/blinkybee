from tornado.ioloop import PeriodicCallback

from blinkybee import settings, utils

class Pattern():
    def __init__(self, bee, pattern):
        self.bee = bee
        self.color = pattern.get('settings')[0]["default"]

    def start(self):
        self.loop = PeriodicCallback(self.draw, 1000)
        self.loop.start()
        self.draw()

    def stop(self):
        self.loop.stop()

    def update(self, options):
        self.color = options.get('color')
        self.draw()

    def draw(self):
        rgb = utils.hex_to_rgb(self.color)
        self.bee.draw([rgb] * settings.PIXEL_COUNT)