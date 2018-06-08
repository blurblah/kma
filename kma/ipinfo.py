
import json
import certifi
import urllib3


class IPInfo(object):
    def __init__(self):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs = certifi.where()
        )
        r = http.request('GET', 'https://ipinfo.io/json')
        self._ipinfo = json.loads(r.data.decode('utf-8'))
        print("Retrieved ip information => {}".format(self._ipinfo))

    def get_location(self):
        location = self._ipinfo['loc'].split(',')
        return {
            'lat': float(location[0]),
            'lon': float(location[1])
        }
