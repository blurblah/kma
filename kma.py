# initial setup
# ip => latitude, longitude => x, y value
# get current / forecast

from xy_converter import Converter
from ipinfo import IPInfo
from current import Current
from forecast import Forecast
from datetime import datetime, timedelta
import pytz
import urllib3
import json
import certifi
from urllib.parse import unquote


class Weather(object):
    DATE_FMT = '%Y%m%d'
    TIME_FMT = '%H%M'
    FORECAST_TIME = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']
    ENDPOINT = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2'

    def __init__(self, api_key):
        self._api_key = api_key
        self.http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )
        self.SERVICE_KEY = 'sample_api_key'

    def _calculate_xy_point(self):
        ip_info = IPInfo()
        location = ip_info.get_location()
        return Converter().convert_coord_to_xy(
            location['lat'],
            location['lon']
        )

    def _get_now(self, fmt):
        now = pytz.utc.localize(datetime.utcnow())
        return pytz.timezone('Asia/Seoul') \
            .normalize(now).strftime(fmt)

    def _get_date(self):
        return self._get_now(self.DATE_FMT)

    def _get_time(self):
        return self._get_now(self.TIME_FMT)

    def get_current(self):
        date = self._get_date()
        time = self._get_time()
        date_param = date
        time_param = time[:2] + '00'
        if int(time[2:]) <= 30:
            if int(time[:2]) == 0:
                # yesterday case
                date_param = (datetime.strptime(date, self.DATE_FMT)
                              - timedelta(days=1)).strftime(self.DATE_FMT)
            temp_time = (datetime.strptime(time, self.TIME_FMT)
                         - timedelta(hours=1)).strftime(self.TIME_FMT)
            time_param = temp_time[:2] + '00'
        body = self._request_api('ForecastGrib', date_param, time_param)['response']['body']
        return Current(self._find_value(body['items']['item'], 'T1H'),
                       self._find_value(body['items']['item'], 'REH'),
                       self._find_value(body['items']['item'], 'SKY'),
                       self._find_value(body['items']['item'], 'RN1'))

    def get_forecast(self):
        date = self._get_date()
        time = self._get_time()
        date_param = date
        # 2, 5, 8, 11, 14, 17, 20, 23 hour
        time_index = int(time[:2]) // 3
        time_offset = int(time[:2]) % 3
        if time_offset == 2:
            if int(time[2:]) <= 10:
                time_index -= 1
        else:
            time_index -= 1

        if time_index < 0:
            date_param = (datetime.strptime(date, self.DATE_FMT)
                          - timedelta(days=1)).strftime(self.DATE_FMT)
            time_index = len(self.FORECAST_TIME) - 1
        time_param = self.FORECAST_TIME[time_index]
        print(self._request_api('ForecastSpaceData', date_param, time_param))

    def _request_api(self, api, base_date, base_time):
        loc = self._calculate_xy_point()
        # service key is encoded and urllib3 request will be encode parameters again
        r = self.http.request('GET', self.ENDPOINT + '/' + api,
                              fields={
                                  'ServiceKey': unquote(self.SERVICE_KEY),
                                  'base_date': base_date,
                                  'base_time': base_time,
                                  'nx': loc['x'],
                                  'ny': loc['y'],
                                  '_type': 'json'
                              })
        return json.loads(r.data.decode('utf-8'))

    def _find_value(self, items, category):
        #return [item for item in items if item['category'] == category]
        for item in items:
            if item['category'] == category:
                return item['obsrValue']
        return None


if __name__ == '__main__':
    w = Weather('api_key')
    curr = w.get_current()
    print(curr.temperature, curr.humidity, curr.sky, curr.rain_drop)
    #print(w.get_date())
    #print(w.get_time())