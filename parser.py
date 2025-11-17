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
        """
        Convert a value to an integer.

        Args:
            value (str | int | None): The value to convert in an integer.

        Returns:
            int | None: Converted integer, or None if conversion fails.
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def log_parsing_warning(filename, row_num, error_type, message):
        """
        Log a parsing warning for invalid or missing data.

        Args:
            filename (str): The name of CSV file.
            row_num (int): The row number in that CSV file.
            error_type (str): Type of error or warning.
            message (str): Message about the warning.
        """
        logging.warning(f"{filename}, row {row_num}: {error_type} - {message}")

    @classmethod
    def parse_directory_to_readings(cls, directory):
        """
        Parse all CSV files in a directory into WeatherReading objects.

        Args:
            directory (str | Path): Path to the directory containing weather CSV files.

        Returns:
            list[WeatherReading]: A list of WeatherReading objects parsed from all files in the directory.
        """
        parsed_weather_readings = []
        dir_path = Path(directory)

        for file_path in dir_path.iterdir():
            parsed_weather_readings.extend(cls.parse_file_to_readings(file_path))

        return parsed_weather_readings

    @classmethod
    def parse_file_to_readings(cls, file_path):
        """
        Parse a single CSV file into WeatherReading objects.

        Args:
            file_path (str | Path): Path to the CSV file to parse.

        Returns:
            list[WeatherReading]: A list of WeatherReading objects parsed from the file.
        """
        weather_readings = []
        with file_path.open("r", encoding="utf-8") as weather_file:
            weather_file_rows = csv.DictReader(weather_file)

            start_line_num = 2 if weather_file_rows.fieldnames else 1

            for row_num, row in enumerate(weather_file_rows, start=start_line_num):
                weather_reading = cls.parse_row_to_reading(row, file_path.name, row_num)
                if weather_reading:
                    weather_readings.append(weather_reading)

            return weather_readings

    @classmethod
    def parse_row_to_reading(cls, row, filename, row_num):
        """
        Parse a single row from a CSV file into a WeatherReading object.

        Args:
            row (dict): A dictionary representing a CSV row.
            filename (str): Name of the file being parsed.
            row_num (int): The row number in the CSV file.

        Returns:
            WeatherReading | None: A WeatherReading object if the row is valid,
            otherwise None if there are missing or invalid values.
        """
        date_column_in_row = DATE_COLUMN if DATE_COLUMN in row else ALTERNATE_DATE_COLUMN
        date_value_from_csv = row.get(date_column_in_row, "").strip()

        if not date_value_from_csv :
            cls.log_parsing_warning(filename, row_num, "MissingColumns",
                                        "Date column missing")
            return None

        try:
            date = datetime.strptime(date_value_from_csv, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            cls.log_parsing_warning(filename, row_num,
                                    "InvalidDate",
                                    f"'{date_value_from_csv}'")
            return None

        numeric_values = {}
        columns_with_invalid_values = []

        for field_key, field_name in NUMERIC_FIELDS.items():
            numeric_value = cls.parse_value_to_int(row.get(field_name))
            numeric_values[field_key] = numeric_value
            if numeric_value is None:
                columns_with_invalid_values.append(field_name)

        if columns_with_invalid_values:
            cls.log_parsing_warning(
                filename,
                row_num,
                "ValueError",
                "Invalid values in: " + ", ".join(columns_with_invalid_values)
            )
            return None

        return WeatherReading(
            date,
            numeric_values["MAX_TEMPERATURE"],
            numeric_values["MIN_TEMPERATURE"],
            numeric_values["MEAN_HUMIDITY"]
        )
