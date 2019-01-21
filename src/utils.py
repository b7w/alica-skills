import logging

import requests
from gunicorn.app.base import BaseApplication
from lxml import html as lh

logger = logging.getLogger(__name__)


class GunicornApplication(BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, logging_dict):
        self.app = app
        self.logging_dict = logging_dict
        super(GunicornApplication, self).__init__()

    def load_config(self):
        self.cfg.set('bind', '0.0.0.0:5000')
        self.cfg.set('workers', '1')
        self.cfg.set('logconfig_dict', self.logging_dict)

    def load(self):
        return self.app.wsgi_app


def retrieve_bash_best():
    r = requests.get('https://bash.im/best')
    doc = lh.fromstring(r.text)
    for quote in doc.cssselect('div.quote'):
        id = quote.cssselect('a.id')[0].text_content().strip()
        lines = list(quote.cssselect('div.text')[0].itertext())
        yield id, lines
