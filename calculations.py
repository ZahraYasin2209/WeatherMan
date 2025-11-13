from constants import (
    MONTHLY_ATTRIBUTE_MAP,
    WEATHER_ATTRIBUTES,
    YEARLY_ATTRIBUTE_MAP,
)


class WeatherCalculator:
    @staticmethod
    def calculate_average(weather_readings):
        valid_weather_readings = [reading for reading in weather_readings
                                if reading is not None]

        return round(sum(valid_weather_readings) / len(valid_weather_readings)) \
            if valid_weather_readings else None

    @staticmethod
    def filter_valid_readings(weather_readings, weather_attributes):
        return {weather_attribute: [reading for reading in weather_readings
                                    if getattr(reading, weather_attribute) is not None]
                for weather_attribute in weather_attributes}

    @staticmethod
    def find_max_readings(readings_dict):
        return {
            weather_attribute: max(weather_readings, key=lambda reading:
                getattr(reading, weather_attribute), default=None)
            for weather_attribute, weather_readings in readings_dict.items()
        }

    @staticmethod
    def filter_readings_by_year_and_month(weather_readings, year, month=None):
        return [reading for reading in weather_readings if reading.date.year == year and
                (month is None or reading.date.month == month)]

    def yearly_calculations(self, weather_readings, year):
        yearly_readings = self.filter_readings_by_year_and_month(weather_readings, year)
        if not yearly_readings:
            return None

        valid_readings = self.filter_valid_readings(yearly_readings, WEATHER_ATTRIBUTES)
        max_values = self.find_max_readings(valid_readings)

        if not any(max_values[attribute] for attribute in WEATHER_ATTRIBUTES):
            return None

        return {key: max_values[attribute] for attribute, key in YEARLY_ATTRIBUTE_MAP.items()}

    def monthly_calculations(self, weather_readings, year, month):
        monthly_readings = self.filter_readings_by_year_and_month(weather_readings, year, month)

        if not monthly_readings:
            return None

        return {key: self.calculate_average(getattr(reading, attribute) for reading in monthly_readings)
                for attribute, key in MONTHLY_ATTRIBUTE_MAP.items()}
