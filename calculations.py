from constants import WEATHER_ATTRIBUTES


class WeatherCalculator:
    @staticmethod
    def calculate_average(values):
        numeric_values = [value for value in values if value is not None]
        return round(sum(numeric_values) / len(numeric_values)) \
            if numeric_values else None

    @staticmethod
    def filter_valid_readings(readings, attributes):
        return {attribute: [reading for reading in readings if getattr(reading, attribute) is not None]
                for attribute in attributes}

    @staticmethod
    def find_max_readings(readings_dict):
        return {
            attribute: max(readings, key=lambda reading: getattr(reading, attribute), default=None)
            for attribute, readings in readings_dict.items()
        }

    @staticmethod
    def filter_by_year_month(readings, year, month=None):
        return [reading for reading in readings if reading.date.year == year and
                (month is None or reading.date.month == month)]

    def yearly_calculations(self, readings, year):
        yearly_readings = self.filter_by_year_month(readings, year)
        if not yearly_readings:
            return None

        valid_readings = self.filter_valid_readings(yearly_readings, WEATHER_ATTRIBUTES)
        max_values = self.find_max_readings(valid_readings)

        if not any(max_values[attribute] for attribute in WEATHER_ATTRIBUTES):
            return None

        yearly_temp = {
            "max_temp": "highest_temperature",
            "min_temp": "lowest_temperature",
            "mean_humidity": "highest_mean_humidity_day"
        }

        return {key: max_values[attribute] for attribute, key in yearly_temp.items()}

    def monthly_calculations(self, readings, year, month):
        monthly_readings = self.filter_by_year_month(readings, year, month)

        if not monthly_readings:
            return None

        monthly_temp = {
            "max_temp": "highest_average_temp",
            "min_temp": "lowest_average_temp",
            "mean_humidity": "average_mean_humidity"
        }

        return {key: self.calculate_average(getattr(reading, attribute) for reading in monthly_readings)
                for attribute, key in monthly_temp.items()}
