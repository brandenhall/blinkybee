import json
import logging

from tornado.web import RequestHandler

logger = logging.getLogger('conductor')

class UpdateHandler(RequestHandler):
    def initialize(self, bee):
        self.bee = bee

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")

        data = json.loads(self.request.body)
        if 'brightness' in data:
            self.bee.set_brightness(data.get('brightness'))

        if 'pattern' in data:
            self.bee.set_pattern(data.get('pattern'))

        if 'options' in data:
            self.bee.set_options(data.get('options'))

        self.write('{"success":true}')