import logging
import os

from api import app

LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL', 'WARNING')

if LOGGING_LEVEL not in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
    raise ValueError(f'Invalid log level: {LOGGING_LEVEL}')

logging.basicConfig(level=LOGGING_LEVEL)
logging.info(f"Streamify server started with {LOGGING_LEVEL} logging level")

if __name__ == '__main__':
    app.run()
