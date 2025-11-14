import csv
import logging
from datetime import datetime
from pathlib import Path

from constants import (
    ALTERNATE_DATE_COLUMN,
    DATE_COLUMN,
    LOG_CONFIG,
    NUMERIC_FIELDS,
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
        dir_path = Path(directory)

        for file_path in dir_path.iterdir():
            with file_path.open('r', encoding='utf-8') as weather_file:
                reader = csv.DictReader(weather_file)

                for row_num, row in enumerate(reader, start=2):
                    date_col = DATE_COLUMN if DATE_COLUMN in row else ALTERNATE_DATE_COLUMN
                    date_value = row.get(date_col, "").strip()

                    if not date_value:
                        cls.log_warning(file_path.name, row_num, "MissingColumns",
                                        "Date column missing")
                        continue

                    try:
                        date = datetime.strptime(date_value, "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        cls.log_warning(file_path.name, row_num,
                                        "InvalidDate",
                                        f"'{date_value}'")
                        continue

                    numeric_values = {}
                    invalid_columns = []

                    for key, field_name in NUMERIC_FIELDS.items():
                        value = cls.parse_value_to_int(row.get(field_name))
                        numeric_values[key] = value
                        if value is None:
                            invalid_columns.append(field_name)

                    if invalid_columns:
                        cls.log_warning(
                            file_path.name,
                            row_num,
                            "ValueError",
                            "Invalid values in: " + ", ".join(invalid_columns)
                        )
                        continue

                    readings.append(
                        WeatherReading(
                            date,
                            numeric_values['MAX_TEMPERATURE'],
                            numeric_values['MIN_TEMPERATURE'],
                            numeric_values['MEAN_HUMIDITY']
                        )
                    )

        return readings
