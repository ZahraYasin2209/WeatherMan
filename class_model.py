class WeatherReadings:
    # holds daily weather data
    def __init__(self, date, max_temp, min_temp, mean_humidity):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.mean_humidity = mean_humidity