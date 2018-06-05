# initial setup
# ip => latitude, longitude => x, y value
# get current / forecast

from xy_converter import Converter
from ipinfo import IPInfo
from current import Current
from forecast import Forecast
from datetime import datetime, timedelta
import pytz


class Weather(object):
    DATE_FMT = '%Y%m%d'
    TIME_FMT = '%H%M'
    FORECAST_TIME = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']

    def __init__(self, api_key):
        self._api_key = api_key

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

        #return Current()

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

        return Forecast()


if __name__ == '__main__':
    w = Weather('api_key')
    w.get_forecast()
    #print(w.get_date())
    #print(w.get_time())