
import certifi
import json
import logging
import pytz
import urllib3
from datetime import datetime, timedelta
from urllib.parse import unquote

from .current import Current
from .exceptions import KMAException
from .forecast import Forecast
from .ipinfo import IPInfo
from .xy_converter import Converter

log = logging.getLogger(__name__)


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
        response = self._request_api('ForecastGrib', date_param, time_param)['response']
        header = response['header']
        if header['resultCode'] == '0000':
            item_list = response['body']['items']['item']
            log.info('Retrieved current weather information.')
            return Current(pytz.timezone('Asia/Seoul')
                           .localize(datetime.strptime(date_param + time_param, '%Y%m%d%H%M')),
                           self._find_current_value(item_list, 'T1H'),
                           self._find_current_value(item_list, 'REH'),
                           self._find_current_value(item_list, 'SKY'),
                           self._find_current_value(item_list, 'RN1'))
        else:
            log.warning('Error response with code:{} and message:{}'
                        .format(header['resultCode'], header['resultMsg']))
            raise KMAException(header['resultCode'], header['resultMsg'])

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
        response = self._request_api('ForecastSpaceData', date_param, time_param)['response']
        header = response['header']
        if header['resultCode'] == '0000':
            item_list = response['body']['items']['item']
            log.info('Retrieved weather forecast information.')
            return Forecast(pytz.timezone('Asia/Seoul')
                            .localize(datetime.strptime(date_param + time_param, '%Y%m%d%H%M')),
                            self._find_forecast_value(item_list, 'T3H'),
                            self._find_forecast_value(item_list, 'TMN'),
                            self._find_forecast_value(item_list, 'TMX'),
                            self._find_forecast_value(item_list, 'REH'),
                            self._find_forecast_value(item_list, 'POP'))
        else:
            log.warning('Error response with code:{} and message:{}'
                        .format(header['resultCode'], header['resultMsg']))
            raise KMAException(header['resultCode'], header['resultMsg'])

    def _request_api(self, api, base_date, base_time):
        loc = self._calculate_xy_point()
        # service key is encoded and urllib3 request will be encode parameters again
        url = self.ENDPOINT + '/' + api
        log.info('Request url: {}'.format(url))
        log.info('with base_date: {}, base_time: {}, nx: {}, ny: {}, _type: json'
                 .format(base_date, base_time, loc['x'], loc['y']))
        r = self.http.request('GET', url,
                              fields={
                                  'ServiceKey': unquote(self._api_key),
                                  'base_date': base_date,
                                  'base_time': base_time,
                                  'nx': loc['x'],
                                  'ny': loc['y'],
                                  '_type': 'json'
                              })
        json_obj = json.loads(r.data.decode('utf-8'))
        log.debug('Response => ' + json.dumps(json_obj, indent=4))
        return json_obj

    def _find_current_value(self, items, category):
        return self._find_value(items, category, 'obsrValue')

    def _find_forecast_value(self, items, category):
        return self._find_value(items, category, 'fcstValue')

    def _find_value(self, items, category, value_name):
        for item in items:
            if item['category'] == category:
                return item[value_name]
        return None
