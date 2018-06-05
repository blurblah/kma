
class Current(object):
    def __init__(self, temperature, humidity, sky, rain_drop=0):
        self.temperature = temperature
        self.humidity = humidity
        self.sky = sky
        self.rain_drop = rain_drop
