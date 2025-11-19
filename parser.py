import csv
import logging
from datetime import datetime
from pathlib import Path

from constants import (
    DATE_COLUMNS,
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
            value_parser = int(value)
        except (ValueError, TypeError):
            value_parser = None

        return value_parser

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

        for file_path in Path(directory).iterdir():
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

            for weather_file_row in weather_file_rows:
                weather_reading = cls.parse_row_to_reading(
                    weather_file_row,
                    file_path.name,
                    weather_file_rows.line_num
                )

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
        weather_reading = None

        date_str_from_csv = cls.get_first_valid_date_value(DATE_COLUMNS, row)

        try:
            date = datetime.strptime(date_str_from_csv, "%Y-%m-%d").date()
            numeric_values = {}
            columns_with_invalid_values = []

            for weather_field_identifier, weather_field_label in NUMERIC_FIELDS.items():
                numeric_value = cls.parse_value_to_int(row.get(weather_field_label))
                numeric_values[weather_field_identifier] = numeric_value

                if numeric_value is None:
                    columns_with_invalid_values.append(weather_field_label)

            if columns_with_invalid_values:
                cls.log_parsing_warning(
                    filename,
                    row_num,
                    "ValueError",
                    "Invalid values in: " + ", ".join(columns_with_invalid_values)
                )
            else:
                weather_reading = WeatherReading(
                    date,
                    numeric_values["MAX_TEMPERATURE"],
                    numeric_values["MIN_TEMPERATURE"],
                    numeric_values["MEAN_HUMIDITY"]
                )
        except (ValueError, TypeError) as date_parse_error:
            cls.log_parsing_warning(
                filename,
                row_num,
                "InvalidDate",
                f"Error parsing date '{date_str_from_csv}': {str(date_parse_error)}"
        )

        return weather_reading

    @classmethod
    def get_first_valid_date_value(cls, date_columns, row):
        """
        Get the first non-empty date value from the provided date columns.

        Args:
            date_columns (list[str]): List of date column names.
            row (dict): The row from which to extract the date.

        Returns:
            str | None: The first non-empty date as a string, or None if no valid date is found.
        """
        valid_date_column_values = (
            row.get(date_column, "").strip()
            for date_column in date_columns
            if row.get(date_column, "").strip()
        )

        return next(valid_date_column_values, None)
