from constants import (
    MONTHLY_ATTRIBUTE_MAP,
    ROUNDED_AVERAGE_PRECISION,
    WEATHER_ATTRIBUTES,
    YEARLY_ATTRIBUTE_MAP,
)
from weather_reading_helpers import WeatherReadingFilter


class WeatherCalculator:
    def __init__(self):
        self.readings = WeatherReadingFilter()

    @staticmethod
    def calculate_average(weather_readings):
        """
        Calculate the average of the given weather readings, ignoring None values.

        Args:
            weather_readings (list[float | int | None]): List of readings

        Returns:
            float: Rounded average if valid readings
        """
        valid_weather_readings = [
            reading for reading in weather_readings if reading
        ]

        if valid_weather_readings:
            average_weather_readings = (
                round(
                    sum(valid_weather_readings) / len(valid_weather_readings),
                    ROUNDED_AVERAGE_PRECISION
                )
            )

            return average_weather_readings

    @staticmethod
    def find_max_reading_per_attribute(attribute_readings):
        """
        Find the maximum reading for each weather attribute.

        Args:
            attribute_readings (dict[str, list[WeatherReading]]):
            Dictionary mapping weather attributes (e.g., "temperature", "humidity") to lists of WeatherReading objects.

        Returns:
            dict[str, WeatherReading | None]: Dictionary mapping each attribute to the WeatherReading
            object that has the maximum value for that attribute.
        """
        max_reading_per_attribute = {}

        for weather_attribute, weather_readings in attribute_readings.items():
            max_reading = max(
                weather_readings,
                key=lambda reading: getattr(reading, weather_attribute)
            )

            max_reading_per_attribute[weather_attribute] = max_reading

        return max_reading_per_attribute

    def calculate_yearly_weather_statistics(self, weather_readings, year):
        """
        Calculate yearly weather statistics for the given year.

        Args:
            weather_readings (list[WeatherReading]): List of weather readings.
            year (int): Year for which calculations are required.

        Returns:
            dict: Dictionary of yearly statistics if valid readings.
        """
        yearly_calculations_result = {}

        yearly_weather_readings = self.readings.get_readings_by_year_and_month(
            weather_readings, year
        )

        if yearly_weather_readings:
            valid_weather_readings = self.readings.get_valid_readings_by_attribute(
                yearly_weather_readings, WEATHER_ATTRIBUTES
            )

            max_values_per_attribute = self.find_max_reading_per_attribute(
                valid_weather_readings
            )

            max_readings_per_attribute = [
                max_values_per_attribute.get(weather_attribute)
                for weather_attribute in WEATHER_ATTRIBUTES
            ]

            if any(max_readings_per_attribute):
                yearly_calculations_result = {
                    yearly_stats_identifier: max_values_per_attribute.get(input_weather_attr)
                    for input_weather_attr, yearly_stats_identifier in YEARLY_ATTRIBUTE_MAP.items()
                }

            return yearly_calculations_result

    def calculate_monthly_weather_statistics(self, weather_readings, year, month):
        """
        Calculate monthly weather statistics for the given year and month.

        Args:
            weather_readings (list[WeatherReading]): List of weather readings.
            year (int): Year for which calculations are required.
            month (int): Month for which calculations are required.

        Returns:
            dict: Dictionary of monthly statistics if valid readings.
        """
        monthly_calculations_result = {}

        monthly_weather_readings = self.readings.get_readings_by_year_and_month(
            weather_readings, year, month
        )

        for weather_attribute, monthly_stats_key in MONTHLY_ATTRIBUTE_MAP.items():
            if not monthly_weather_readings:
                continue

            weather_attribute_values = [
                getattr(reading, weather_attribute, None)
                for reading in monthly_weather_readings
            ]

            monthly_calculations_result[monthly_stats_key] = self.calculate_average(
                weather_attribute_values
            )

        return monthly_calculations_result
