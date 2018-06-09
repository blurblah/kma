
import logging

from .current import Current
from .forecast import Forecast
from .kma import Weather

__author__ = 'blurblah (blurblah@blurblah.net)'
__license__ = 'MIT'
__version__ = '0.2.0'

__all__ = (
    'Weather',
    'Current',
    'Forecast'
)

logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

logger.addHandler(handler)
logger.setLevel(logging.INFO)
