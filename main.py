import logging
import os

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'WARNING')

if LOGGING_LEVEL not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
    raise ValueError(f'Invalid log level: {LOGGING_LEVEL}')

logging.basicConfig(level=LOGGING_LEVEL)

from app import app

if __name__ == '__main__':
    app.run()
