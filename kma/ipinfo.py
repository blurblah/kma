
import certifi
import json
import logging
import urllib3

log = logging.getLogger(__name__)


class IPInfo(object):
    def __init__(self):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs = certifi.where()
        )
        r = http.request('GET', 'https://ipinfo.io/json')
        self._ipinfo = json.loads(r.data.decode('utf-8'))
        log.debug("Retrieved ip information => {}".format(self._ipinfo))

    def get_location(self):
        location = self._ipinfo['loc'].split(',')
        return {
            'lat': float(location[0]),
            'lon': float(location[1])
        }
