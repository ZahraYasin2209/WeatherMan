from constants import (
    MONTHLY_ATTRIBUTE_MAP,
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
            float | None: Rounded average or None if no valid readings
        """
        valid_weather_readings = [
            reading for reading in weather_readings
            if reading]

        if not valid_weather_readings:
            return None

        average_weather_readings = sum(valid_weather_readings) / len(valid_weather_readings)

        return round(average_weather_readings, 2)

    @staticmethod
    def find_max_values_per_attribute(attribute_readings):
        """
        Find the maximum reading for each weather attribute.

        Args:
            attribute_readings (dict[str, list[WeatherReading]]):
            Dictionary mapping weather attributes (e.g., "temperature", "humidity") to lists of WeatherReading objects.

        Returns:
            dict[str, WeatherReading | None]: Dictionary mapping each attribute to the WeatherReading
            object that has the maximum value for that attribute.
            Returns None if no readings exist for an attribute.
        """
        max_reading_per_attribute = {}

        for attribute, weather_readings in attribute_readings.items():
            if weather_readings:
                max_reading_per_attribute[attribute] = max(weather_readings,
                                                           key=lambda reading: getattr(reading, attribute))
            else:
                max_reading_per_attribute[attribute] = None

        return max_reading_per_attribute

    def calculate_yearly_weather_statistics(self, weather_readings, year):
        """
        Calculate yearly weather statistics for the given year.

        Args:
            weather_readings (list[WeatherReading]): List of weather readings.
            year (int): Year for which calculations are required.

        Returns:
            dict | None: Dictionary of yearly statistics or None if no valid readings.
        """
        yearly_calculations_result = None

        yearly_readings = self.readings.filter_readings_by_year_and_month(weather_readings, year)

        if yearly_readings:
            valid_weather_readings = self.readings.filter_valid_readings(yearly_readings, WEATHER_ATTRIBUTES)

            max_values_per_attribute = self.find_max_values_per_attribute(valid_weather_readings)

            if any(max_values_per_attribute.get(attribute) for attribute in WEATHER_ATTRIBUTES):
                yearly_calculations_result = {
                    output_key: max_values_per_attribute.get(input_attr)
                    for input_attr, output_key in YEARLY_ATTRIBUTE_MAP.items()
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
            dict | None: Dictionary of monthly statistics or None if no valid readings.
        """
        monthly_calculations_result = None

        monthly_weather_readings = self.readings.filter_readings_by_year_and_month(weather_readings, year, month)

        if monthly_weather_readings:
            monthly_calculations_result = {}
            for weather_attribute, output_key in MONTHLY_ATTRIBUTE_MAP.items():
                weather_attribute_values = [
                    getattr(weather_reading, weather_attribute)
                    for weather_reading in monthly_weather_readings
                    if hasattr(weather_reading, weather_attribute)
                       and getattr(weather_reading, weather_attribute) is not None
                ]
                monthly_calculations_result[output_key] = self.calculate_average(weather_attribute_values)

        return monthly_calculations_result
