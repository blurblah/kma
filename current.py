
class Current(object):
    def __init__(self, basetime, temperature, humidity, sky, rain_drop=0):
        self.basetime = basetime
        self.temperature = temperature
        self.humidity = humidity
        self.sky = sky  # sky value : 1(clear), 2, 3, 4(cloudy)
        self.rain_drop = rain_drop  # including snow
