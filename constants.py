from pathlib import Path

WEATHER_DIRECTORY = "weatherfiles"
CURRENT_SCRIPT_DIRECTORY = Path(__file__).resolve().parent
WEATHER_PROJECT_DIRECTORY = CURRENT_SCRIPT_DIRECTORY.parents[1]
DEFAULT_WEATHER_DIR_PATH = WEATHER_PROJECT_DIRECTORY / WEATHER_DIRECTORY

AVERAGE_DEFAULT_VALUE = 0.0
DATE_COLUMNS = ["PKT", "PKST"]
LOG_FILE = "weatherman_log_errors.log"
MAX_TEMPERATURE = "Max TemperatureC"
MEAN_HUMIDITY = " Mean Humidity"
MIN_TEMPERATURE = "Min TemperatureC"
ROUNDED_AVERAGE_PRECISION = 2
WEATHER_ATTRIBUTES = ["max_temp", "min_temp", "mean_humidity"]

RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"

MONTHLY_ATTRIBUTE_MAP = {
    "max_temp": "highest_average_temp",
    "min_temp": "lowest_average_temp",
    "mean_humidity": "average_mean_humidity"
}

LOG_CONFIG = {
    "filename": LOG_FILE,
    "level": "WARNING",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
}

NUMERIC_FIELDS = {
    "MAX_TEMPERATURE": "Max TemperatureC",
    "MIN_TEMPERATURE": "Min TemperatureC",
    "MEAN_HUMIDITY": " Mean Humidity"
}

YEARLY_ATTRIBUTE_MAP = {
    "max_temp": "highest_temperature",
    "min_temp": "lowest_temperature",
    "mean_humidity": "highest_mean_humidity_day"
}
