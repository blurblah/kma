
class Current(object):
    def __init__(self, basetime, temperature, humidity, sky, rain_drop=0):
        self.basetime = basetime
        self.temperature = temperature
        self.humidity = humidity
        self.rain_drop = rain_drop  # including snow
