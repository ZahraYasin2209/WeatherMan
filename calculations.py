from constants import (
    MONTHLY_ATTRIBUTE_MAP,
    WEATHER_ATTRIBUTES,
    YEARLY_ATTRIBUTE_MAP,
)
from weather_reading_utils import WeatherReadingFilter


class WeatherCalculator:
    def __init__(self):
        self.readings = WeatherReadingFilter()

    @staticmethod
    def calculate_average(weather_readings):
        valid_weather_readings = [reading for reading in weather_readings
                                if reading is not None]

        return round(sum(valid_weather_readings) / len(valid_weather_readings)) \
            if valid_weather_readings else None

    @staticmethod
    def find_max_readings(readings_dict):
        return {
            weather_attribute: max(weather_readings, key=lambda reading:
                getattr(reading, weather_attribute), default=None)
            for weather_attribute, weather_readings in readings_dict.items()
        }

    def yearly_calculations(self, weather_readings, year):
        yearly_readings = self.readings.filter_readings_by_year_and_month(weather_readings, year)
        if not yearly_readings:
            return None

        valid_readings = self.readings.filter_valid_readings(yearly_readings, WEATHER_ATTRIBUTES)
        max_values = self.find_max_readings(valid_readings)

        if not any(max_values[attribute] for attribute in WEATHER_ATTRIBUTES):
            return None

        return {key: max_values[attribute] for attribute, key in YEARLY_ATTRIBUTE_MAP.items()}

    def monthly_calculations(self, weather_readings, year, month):
        monthly_readings = self.readings.filter_readings_by_year_and_month(weather_readings, year, month)

        if not monthly_readings:
            return None

        return {key: self.calculate_average(getattr(reading, attribute) for reading in monthly_readings)
                for attribute, key in MONTHLY_ATTRIBUTE_MAP.items()}
