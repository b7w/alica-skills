import logging

from gunicorn.app.base import BaseApplication

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
