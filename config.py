import os
import logging
from decouple import config


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = config('DATABASE_URI')
TELEGRAM_TOKEN = config('TELEGRAM_TOKEN')
DRIVERS_DIR = os.path.join(BASEDIR, 'drivers')
