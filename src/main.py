#!/usr/bin/env python

import logging
import random
from logging.config import dictConfig

from flask import Flask, request, jsonify

from utils import GunicornApplication, retrieve_bash_best

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
