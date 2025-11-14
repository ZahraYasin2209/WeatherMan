DIRECTORY_PATH = "/Users/macbook/PycharmProjects/PythonProject/Weather Project/weatherfiles"

MAX_TEMPERATURE = "Max TemperatureC"
MIN_TEMPERATURE = "Min TemperatureC"
MEAN_HUMIDITY = " Mean Humidity"
WEATHER_ATTRIBUTES = ["max_temp", "min_temp", "mean_humidity"]
LOG_FILE = "log_errors.log"
DATE_COLUMN = "PKT"
ALTERNATE_DATE_COLUMN = "PKST"

RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"

MONTHLY_ATTRIBUTE_MAP = {
    "max_temp": "highest_average_temp",
    "min_temp": "lowest_average_temp",
    "mean_humidity": "average_mean_humidity"
}

YEARLY_ATTRIBUTE_MAP = {
    "max_temp": "highest_temperature",
    "min_temp": "lowest_temperature",
    "mean_humidity": "highest_mean_humidity_day"
}

LOG_CONFIG = {
    "filename": LOG_FILE,
    "level": "WARNING",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}

NUMERIC_FIELDS = {
    'MAX_TEMPERATURE': 'Max TemperatureC',
    'MIN_TEMPERATURE': 'Min TemperatureC',
    'MEAN_HUMIDITY': ' Mean Humidity'
}
