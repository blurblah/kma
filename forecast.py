
class Forecast(object):
    def __init__(self, min_temperature, max_temperature,
                 humidity, rain_probability):
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.humidity = humidity
        self.rain_probability = rain_probability
