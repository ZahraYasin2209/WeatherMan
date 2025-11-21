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
    def parse_value_to_int(raw_value):
        """
        Convert a value to an integer.

        Args:
            raw_value (str | int | None): The value to convert in an integer.

        Returns:
            int | None: Converted integer, or None if conversion fails.
        """
        try:
            parsed_integer_value = int(raw_value)
        except (ValueError, TypeError):
            parsed_integer_value = None

        return parsed_integer_value

    @staticmethod
    def log_parsing_warning(weather_file_name, row_num, error_type, message):
        """
        Log a parsing warning for invalid or missing data.

        Args:
            weather_file_name (str): The name of CSV file.
            row_num (int): The row number in that CSV file.
            error_type (str): Type of error or warning.
            message (str): Message about the warning.
        """
        logging.warning(f"{weather_file_name}, row {row_num}: {error_type} - {message}")

    @classmethod
    def parse_directory_to_readings(cls, directory):
        """
        Parse all CSV files in a directory into WeatherReading objects.

        Args:
            directory (str): Path to the directory containing weather CSV files.

        Returns:
            list[WeatherReading]: A list of WeatherReading objects parsed from all files in the directory.
        """
        parsed_weather_readings = []

        for weather_data_file in Path(directory).iterdir():
            parsed_weather_readings.extend(cls.parse_file_to_readings(weather_data_file))

        return parsed_weather_readings

    @classmethod
    def parse_file_to_readings(cls, weather_file_path):
        """
        Parse a single CSV file into WeatherReading objects.

        Args:
            weather_file_path (str | Path): Path to the CSV file to parse.

        Returns:
            list[WeatherReading]: A list of WeatherReading objects parsed from the file.
        """
        weather_readings = []

        with weather_file_path.open("r", encoding="utf-8") as weather_file:
            weather_file_rows = csv.DictReader(weather_file)

            for weather_file_row in weather_file_rows:
                weather_reading = cls.parse_row_to_reading(
                    weather_file_row,
                    weather_file_path.name,
                    weather_file_rows.line_num
                )

                if weather_reading:
                    weather_readings.append(weather_reading)

        return weather_readings

    @classmethod
    def parse_row_to_reading(cls, weather_file_row, weather_file_name, weather_file_row_num):
        """
        Parse a single row from a CSV file into a WeatherReading object.

        Args:
            weather_file_row (dict): A dictionary representing a CSV row.
            weather_file_name (str): Name of the file being parsed.
            weather_file_row_num (int): The row number in the CSV file.

        Returns:
            WeatherReading | None: A WeatherReading object if the row is valid,
            otherwise None if there are missing or invalid values.
        """
        date_str_from_csv = next(
            (
                date_column_value
                for date_column in DATE_COLUMNS
                if (date_column_value := weather_file_row.get(date_column, "").strip())
            ),
            None
        )

        try:
            date = datetime.strptime(date_str_from_csv, "%Y-%m-%d").date()
            numeric_values = {}

            for weather_field_identifier, weather_field_label in NUMERIC_FIELDS.items():
                numeric_value = cls.parse_value_to_int(weather_file_row.get(
                    weather_field_label
                ))
                numeric_values[weather_field_identifier] = numeric_value

            return WeatherReading(
                date,
                numeric_values["MAX_TEMPERATURE"],
                numeric_values["MIN_TEMPERATURE"],
                numeric_values["MEAN_HUMIDITY"]
            )
        except (ValueError, TypeError) as date_parse_error:
            cls.log_parsing_warning(
                weather_file_name,
                weather_file_row_num,
                "InvalidDate",
                f"Error parsing date '{date_str_from_csv}': {str(date_parse_error)}"
        )


class InputDateParser:
    @staticmethod
    def parse_and_validate_year(raw_input_year):
        """
        Parse and validate an YEAR given by user (through CLI arguments).

        Args:
            raw_input_year (int): Year to validate.

        Returns:
            int: Validated year.

        Raises:
            ValueError: If the input is not a valid YEAR or in incorrect format.
        """
        try:
            year = int(raw_input_year)

            if year <= 0:
                raise ValueError

            return year
        except ValueError:
            raise ValueError(f"Invalid format for year: {raw_input_year}. Please use YEAR Format")

    @staticmethod
    def parse_and_validate_year_month(raw_year_month):
        """
        Parse and validate a YEAR/MONTH string given by user (through CLI arguments).

        Args:
            raw_year_month (str): String in the format "YEAR/MONTH".

        Returns:
            tuple[int, int]: year and month as integers.

        Raises:
            ValueError: If the input is not in the correct format.
        """
        try:
            year, month = map(int, raw_year_month.split("/"))

            return year, month
        except ValueError:
            raise ValueError(
                f"Invalid format for monthly report: {raw_year_month}. Please use YEAR/MONTH Format"
            )
