import os
import csv
from datetime import datetime

from weather_reading import WeatherReading
from constants import *


""" Helper function to parse string value into int """
def parsing_optional_int(value):
    try:
        return int(value)
    except ValueError:
        return None


""" Parse all weather files present in directory """
def parse_weather_files(directory):
    readings = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory,
                                 filename)

        if os.path.isdir(file_path):
            continue
        if not filename.endswith(".txt"):
            continue

        with open(file_path, 'r') as file:
            weather_readings = csv.DictReader(file)
            for row in weather_readings:
                try:
                    date = datetime.strptime(row["PKT"],"%Y-%m-%d").date()
                    max_temp = parsing_optional_int(row[MAX_TEMPERATURE])
                    min_temp = parsing_optional_int(row[MIN_TEMPERATURE])
                    mean_humidity = parsing_optional_int(row[MEAN_HUMIDITY])

                    readings.append(WeatherReading(date, max_temp, min_temp, mean_humidity))
                except (ValueError, KeyError):
                    continue
    return readings
