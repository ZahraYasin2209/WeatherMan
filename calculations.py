from constants import (
    AVERAGE_DEFAULT_VALUE,
    MONTHLY_ATTRIBUTE_MAP,
    ROUNDED_AVERAGE_PRECISION,
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
            monthly_weather_readings (list[WeatherReading]): List of weather readings for the month.

        Returns:
            dict: A dictionary mapping each average key to its calculated average.
        """
        return {
            monthly_average_key: self.validator.validate_and_calculate_average_for_attribute(
                monthly_weather_readings, weather_attribute
            )
            for weather_attribute, monthly_average_key in MONTHLY_ATTRIBUTE_MAP.items()
        }

    @staticmethod
    def find_max_reading_per_attribute(attribute_readings):
        """
        Find the maximum reading for each weather attribute.

        Args:
            attribute_readings (dict[str, list[WeatherReading]]):
            Dictionary mapping weather attributes (e.g., "temperature", "humidity")
            to lists of WeatherReading objects.

        Returns:
            dict[str, WeatherReading | None]: Dictionary mapping each attribute to the WeatherReading
            object that has the maximum value for that attribute.
        """
        max_reading_per_attribute = {}

        for weather_attribute, weather_readings_for_attribute in attribute_readings.items():
            if weather_readings_for_attribute:
                max_reading = max(
                    weather_readings_for_attribute,
                    key=lambda reading: getattr(reading, weather_attribute)
                )

                max_reading_per_attribute[weather_attribute] = max_reading

        return max_reading_per_attribute

    def calculate_yearly_weather_statistics(self, valid_weather_readings):
        """
        Calculate yearly weather statistics for the given year.

        Args:
            valid_weather_readings (list[WeatherReading]): List of validated weather readings.

        Returns:
            dict: Dictionary of yearly statistics having valid readings.
        """
        max_values_per_attribute = self.find_max_reading_per_attribute(valid_weather_readings)

        return self.readings.get_yearly_max_weather_values(max_values_per_attribute)

    def calculate_monthly_weather_statistics(self, monthly_weather_readings):
        """
        Calculate monthly weather statistics from a list of weather readings.

        Args:
            monthly_weather_readings (list[WeatherReading]): List of weather readings for a specific month.

        Returns:
            dict: A dictionary containing calculated monthly averages
            if readings are available.
        """

        if monthly_weather_readings:
            return self.calculate_monthly_averages(monthly_weather_readings)
