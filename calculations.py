from constants import (
    AVERAGE_DEFAULT_VALUE,
    MONTHLY_ATTRIBUTE_MAP,
    ROUNDED_AVERAGE_PRECISION,
    WEATHER_ATTRIBUTES,
)
from validations import WeatherReadingValidator
from weather_reading_helpers import WeatherReadingFilter


class WeatherCalculator:
    def __init__(self):
        self.readings = WeatherReadingFilter()
        self.validator = WeatherReadingValidator()

    @staticmethod
    def calculate_average(weather_readings):
        """
        Calculate the average of the given weather readings, ignoring None values.

        Args:
            weather_readings (list[float | int | None]): List of numeric weather readings

        Returns:
            float: Rounded average if valid readings else AVERAGE_DEFAULT_VALUE
        """
        average_readings = (
            sum(weather_readings) / len(weather_readings)
            if weather_readings else AVERAGE_DEFAULT_VALUE
        )
        average_weather_readings = round(average_readings, ROUNDED_AVERAGE_PRECISION)

        return average_weather_readings

    def calculate_monthly_averages(self, monthly_weather_readings):
        """
        Calculate averages for all attributes of a monthly weather dataset.

        Args:
            monthly_weather_readings (list[WeatherReading]): List of weather readings.

        Returns:
            dict: Dictionary mapping monthly attribute keys to their averages.
        """
        average_monthly_weather_readings = {}

        for weather_attribute, average_key in MONTHLY_ATTRIBUTE_MAP.items():
            monthly_attribute_values = self.readings.get_attribute_values(
                monthly_weather_readings, weather_attribute
            )

            valid_weather_readings = self.validator.validate_weather_readings(monthly_attribute_values)

            average_monthly_weather_readings[average_key] = self.calculate_average(valid_weather_readings)

        return average_monthly_weather_readings

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
            year (int): Year for which weather reading calculations are required.

        Returns:
            dict: Dictionary of yearly statistics if valid readings.
        """
        yearly_calculations_result = None

        yearly_weather_readings = self.readings.get_yearly_weather_readings(
            weather_readings, year
        )

        valid_weather_readings = self.validator.validate_yearly_weather_readings_by_attribute(
            yearly_weather_readings, WEATHER_ATTRIBUTES
        )

        if self.readings.get_all_attributes_with_valid_readings(valid_weather_readings):
            max_values_per_attribute = self.find_max_reading_per_attribute(valid_weather_readings)
            yearly_calculations_result = self.readings.get_yearly_max_weather_values(max_values_per_attribute)

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
        monthly_weather_readings = self.readings.get_sorted_readings_by_year_and_month(
            weather_readings, year, month
        )

        if monthly_weather_readings:
            return self.calculate_monthly_averages(monthly_weather_readings)
