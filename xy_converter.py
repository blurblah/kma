
import math


# 아래 링크에 있는 javascript 참고해서 정리한 클래스
# http://www.weather.go.kr/weather/forecast/digital_forecast.jsp?x=60&y=127
class Converter(object):
    RE = 6371.00877 # 지구반경(km)
    GRID = 5.0 # 격자 간격(km)
    SLAT1 = 30.0 # 투영 위도1(degree)
    SLAT2 = 60.0 # 투영 위도2(degree)
    OLON = 126.0 # 기준점 경도(degree)
    OLAT = 38.0 # 기준점 위도(degree)
    XO = 43 # 기준점 X좌표(GRID)
    YO = 136 # 기1준점 Y좌표(GRID)

    def __init__(self):
        self._DEGRAD = math.pi / 180.0
        self._RADDEG = 180.0 / math.pi
        self._base = self._calc_base()

    def _calc_base(self):
        re = self.RE / self.GRID
        _slat1 = self.SLAT1 * self._DEGRAD
        _slat2 = self.SLAT2 * self._DEGRAD
        olon = self.OLON * self._DEGRAD
        olat = self.OLAT * self._DEGRAD

        sn = math.tan(math.pi*0.25 + _slat2*0.5) / math.tan(math.pi*0.25 + _slat1*0.5)
        sn = math.log(math.cos(_slat1) / math.cos(_slat2)) / math.log(sn)
        sf = math.tan(math.pi*0.25 + _slat1*0.5)
        sf = math.pow(sf, sn) * math.cos(_slat1) / sn
        ro = math.tan(math.pi*0.25 + olat*0.5)
        ro = re * sf / math.pow(ro, sn)
        return {
            're': re,
            'olon': olon,
            'sn': sn,
            'sf': sf,
            'ro': ro
        }

    def convert_coord_to_xy(self, lat, lon):
        ra = math.tan((math.pi * 0.25) + (lat * self._DEGRAD * 0.5))
        ra = self._base['re'] * self._base['sf'] / math.pow(ra, self._base['sn'])
        theta = lon * self._DEGRAD - self._base['olon']
        if theta > math.pi:
            theta -= 2.0 * math.pi
        elif theta < -math.pi:
            theta += 2.0 * math.pi
        theta *= self._base['sn']
        return {
            'x': math.floor(ra * math.sin(theta) + self.XO + 0.5),
            'y': math.floor(self._base['ro'] - ra * math.cos(theta) + self.YO + 0.5)
        }

    def convert_xy_to_coord(self, x, y):
        base = self._calc_base()

        xn = x - self.XO
        yn = base['ro'] - y + self.YO
        ra = math.sqrt(xn*xn + yn*yn)
        if base['sn'] < 0.0:
            ra = -ra
        alat = math.pow(base['re'] * base['sf'] / ra, 1.0 / base['sn'])
        alat = 2.0 * math.atan(alat) - math.pi*0.5

        if math.fabs(xn) <= 0.0:
            theta = 0.0
        else:
            if math.fabs(yn) <= 0.0:
                theta = math.pi * 0.5
                if xn < 0.0:
                    theta = -theta
            else:
                theta = math.atan2(xn, yn)
        alon = theta / base['sn'] + base['olon']
        return {
            'lat': alat * self._RADDEG,
            'lon': alon * self._RADDEG
        }


if __name__ == '__main__':
    converter = Converter()
    print(converter.convert_coord_to_xy(37.579871,126.989352))
    print(converter.convert_xy_to_coord(60, 127))
