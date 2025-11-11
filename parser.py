import csv
import os
from datetime import datetime

from constants import (
    MAX_TEMPERATURE,
    MIN_TEMPERATURE,
    MEAN_HUMIDITY
)
from weather_reading import WeatherReading


class WeatherDataParser:
    @staticmethod
    def parse_value_to_int(value):
        try:
            return int(value)
        except ValueError:
            return None

    @classmethod
    def parse_directory(cls, directory):
        """Parse all text files in a directory and return WeatherReading objects.

        Args:
            directory (str): Path to directory containing weather text files.

        Returns:
            list[WeatherReading]: List of parsed readings.
        """
        readings = []
        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)
            if os.path.isdir(path) or not filename.endswith(".txt"):
                continue

            with open(path, 'r') as weather_file:
                reader = csv.DictReader(weather_file)
                for row in reader:
                    try:
                        date = datetime.strptime(row["PKT"], "%Y-%m-%d").date()
                        readings.append(
                            WeatherReading(
                                date,
                                cls.parse_value_to_int(row[MAX_TEMPERATURE]),
                                cls.parse_value_to_int(row[MIN_TEMPERATURE]),
                                cls.parse_value_to_int(row[MEAN_HUMIDITY]),
                            )
                        )
                    except (ValueError, KeyError):
                        continue
        return readings
