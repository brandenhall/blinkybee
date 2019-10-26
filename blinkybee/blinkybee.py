import colorsys
import json
import logging
import logging.config
import importlib
import signal
import socket
import time

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.web import Application, StaticFileHandler

from . import handlers, opc, settings

logger = logging.getLogger('conductor')

class BlinkyBee:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.brightness = 0.5
        self.patterns = {}
        self.current_pattern = None

        logging.config.dictConfig(settings.LOGGING)
        signal.signal(signal.SIGTERM, self.on_signal)
        signal.signal(signal.SIGINT, self.on_signal)

        self.opc_client = opc.Client('localhost:7890')

        web_handlers = [
            (r'/update', handlers.UpdateHandler, {"bee": self}),
            (r'/(.*)', StaticFileHandler, {
                'path': settings.WEB_ROOT,
                'default_filename': 'index.html'}),
        ]

        application = Application(web_handlers)
        self.http_server = HTTPServer(application)

    def load(self):
        logger.info('Loading patterns...')
        with open('web/patterns.json', 'r') as f:
            pattern_data = json.loads(f.read())

        for pattern_id, pattern_info in pattern_data.items():
            module = importlib.import_module(pattern_info.get('module'))
            PatternClass = getattr(module, 'Pattern')
            self.patterns[pattern_id] = PatternClass(self, pattern_info)

        self.set_pattern('solid_color')
            

    def draw(self, pixels):
        self.pixels = pixels
        self.blit()
        self.blit()

    def blit(self):
        adjusted = []
        for r, g, b in self.pixels:
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            v *= self.brightness
            rc, gc, bc = colorsys.hsv_to_rgb(h, s, v)
            adjusted.append((
                round(rc * 255.0),
                round(gc * 255.0),
                round(bc * 255.0),
            ))

        self.opc_client.put_pixels(adjusted)

    def set_color(self, r, g, b):
        self.pixels = [(r, g, b)] * settings.PIXEL_COUNT
        self.blit()
        self.blit()

    def clear(self):
        self.set_color(0, 0, 0)

    def set_brightness(self, brightness):
        self.brightness = int(brightness)/100.0
        self.current_pattern.draw()

    def set_pattern(self, pattern):
        if self.current_pattern is not None:
            self.current_pattern.stop()
        self.current_pattern = self.patterns.get(pattern)
        self.current_pattern.start()

    def set_options(self, options):
        self.current_pattern.update(options)

    def start(self):
        self.load()

        logger.info('Starting BlinkyBee...')

        self.clear()
        self.set_color(255, 0, 0)
        time.sleep(0.5)
        self.set_color(0, 255, 0)
        time.sleep(0.5)
        self.set_color(0, 0, 255)
        time.sleep(0.5)
        self.set_color(0, 0, 0)

        logger.info('Listening for HTTP on port {}'.format(settings.HTTP_PORT))

        self.http_server.listen(settings.HTTP_PORT)

        IOLoop.instance().start()

    async def shutdown(self):
        logger.info('Stopping BlinkyBee...')

        try:
            self.clear()
            self.http_server.stop()
            await self.http_server.close_all_connections()
            

        except Exception as e:
            logger.error("Couldn't close connections gracefully")
            logger.exception(e)

        logger.info('Shutdown')
        IOLoop.instance().stop()

    def on_signal(self, sig, frame):
        logger.warning('Caught signal: %s', sig)
        IOLoop.instance().add_callback_from_signal(self.shutdown)


if __name__ == '__main__':
    bb = BlinkyBee()
    bb.start()
