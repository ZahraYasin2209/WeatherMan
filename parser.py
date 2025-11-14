import csv
import logging
import os
from datetime import datetime

from constants import (
    ALTERNATE_DATE_COLUMN,
    DATE_COLUMN,
    MAX_TEMPERATURE,
    MEAN_HUMIDITY,
    MIN_TEMPERATURE,
    LOG_CONFIG,
)
from weather_reading import WeatherReading

logging.basicConfig(
    filename=LOG_CONFIG["filename"],
    level=getattr(logging, LOG_CONFIG["level"]),
    format=LOG_CONFIG["format"],
    datefmt=LOG_CONFIG["datefmt"]
)


class WeatherDataParser:
    @staticmethod
    def parse_value_to_int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def log_warning(filename, row_num, error_type, message):
        logging.warning(f"{filename}, row {row_num}: {error_type} - {message}")

    @classmethod
    def parse_directory(cls, directory):
        readings = []

        for filename in os.listdir(directory):
            path = os.path.join(directory, filename)

            if os.path.isdir(path) or not filename.endswith(".txt"):
                continue

            with (open(path, 'r', encoding='utf-8') as weather_file):
                reader = csv.DictReader(weather_file)

                if not reader.fieldnames:
                    cls.log_warning(filename, 0,
                                    "FileError",
                                    "No header found")
                    continue

                for row_num, row in enumerate(reader, start=2):
                    if all(not (valid_values and valid_values.strip())
                           for valid_values in row.values()):
                        continue

                    date_col = (
                        DATE_COLUMN if DATE_COLUMN in row
                        else ALTERNATE_DATE_COLUMN if ALTERNATE_DATE_COLUMN in row
                        else None
                    )

                    required_columns = [MAX_TEMPERATURE, MIN_TEMPERATURE, MEAN_HUMIDITY]

                    if date_col:
                        required_columns.append(date_col)

                    missing_columns = [col for col in required_columns
                                       if col not in row or not row[col].strip()]

                    if missing_columns:
                        cls.log_warning(filename, row_num,
                                        "MissingColumns", ", ".join(missing_columns))
                        continue

                    try:
                        date = datetime.strptime(row[date_col], "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        cls.log_warning(filename, row_num,
                                        "InvalidDate",
                                        f"'{row.get(date_col)}'")
                        continue

                    numeric_values = {
                        MAX_TEMPERATURE: cls.parse_value_to_int(row[MAX_TEMPERATURE]),
                        MIN_TEMPERATURE: cls.parse_value_to_int(row[MIN_TEMPERATURE]),
                        MEAN_HUMIDITY: cls.parse_value_to_int(row[MEAN_HUMIDITY])
                    }

                    invalid_columns = [col for col, numeric_value in numeric_values.items()
                                       if numeric_value is None]

                    if invalid_columns:
                        cls.log_warning(filename, row_num,
                                        "ValueError", "Invalid values in: "
                                            + ", ".join(invalid_columns))
                        continue

                    readings.append(
                        WeatherReading(
                            date,
                            numeric_values[MAX_TEMPERATURE],
                            numeric_values[MIN_TEMPERATURE],
                            numeric_values[MEAN_HUMIDITY]
                        )
                    )

        return readings
