
class Forecast(object):
    def __init__(self, basetime, temperature_3h,
                 min_temperature, max_temperature,
                 humidity, rain_probability):
        self.basetime = basetime
        self.temperature_3h = temperature_3h
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.humidity = humidity
        self.rain_probability = rain_probability
