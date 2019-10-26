from tornado.ioloop import PeriodicCallback

from blinkybee import settings
from PIL import Image

class Pattern():
    def __init__(self, bee, info):
        self.bee = bee
        self.im = Image.open(info.get('settings')[0].get('default'))
        self.im = self.im.convert('RGB')
        self.im_data = list(self.im.getdata())
        _, self.total_frames = self.im.size
        self.frame = 0
        self.speed = int(info.get('settings')[1].get('default'))

    def start(self):
        self.loop = PeriodicCallback(self.draw, 1000/self.speed)
        self.loop.start()
        self.draw()

    def stop(self):
        self.loop.stop()

    def update(self, options):
        if 'animation' in options:
            self.im = Image.open(options.get('animation'))
            self.im = self.im.convert('RGB')
            self.im_data = list(self.im.getdata())
            _, self.total_frames = self.im.size
            self.frame = 1
        if 'speed' in options:
            self.speed = int(options.get('speed'))
            self.loop.stop()
            self.loop = PeriodicCallback(self.draw, 1000/self.speed)
            self.loop.start()

    def draw(self):
        start = self.frame * 87
        end = start + 87
        self.bee.draw(self.im_data[start:end])

        self.frame += 1
        if self.frame >= self.total_frames:
            self.frame = 0
        