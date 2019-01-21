#!/usr/bin/env python

import logging
import random
from logging.config import dictConfig

import requests
from flask import Flask, request, jsonify
from lxml import html as lh

from .utils import GunicornApplication

logger = logging.getLogger('root')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] [%(name)s.%(funcName)s at %(lineno)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
    },
    'handlers': {
        'simple': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'gunicorn': {
            'handlers': ['simple'],
            'level': 'INFO',
        },
        'flask': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        },
        'root': {
            'handlers': ['simple'],
            'level': 'DEBUG',
        }
    },
}

app = Flask(__name__)


def retrieve_bash_best():
    r = requests.get('https://bash.im/best')
    doc = lh.fromstring(r.text)
    for quote in doc.cssselect('div.quote'):
        id = quote.cssselect('a.id')[0].text_content().strip()
        lines = list(quote.cssselect('div.text')[0].itertext())
        yield id, lines


@app.route('/bash-im', methods=['GET', 'POST'])
def bash_im():
    quotes = list(l for i, l in retrieve_bash_best() if sum(map(len, l)) < 300)
    text = '\n'.join(random.choice(quotes))
    if request.method == 'GET':
        return text

    req = request.json
    logging.info('Request: %r', req)
    response = {
        "version": req['version'],
        "session": req['session'],
        "response": {
            "text": text,
            "end_session": True
        }
    }
    return jsonify(response)


if __name__ == '__main__':
    dictConfig(LOGGING)
    logger.info('STArt')
    GunicornApplication(app, LOGGING).run()
