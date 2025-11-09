class WeatherCalculator:
    @staticmethod
    def calculate_average(values):
        valid_values = [valid for valid in values if valid is not None]
        return round(sum(valid_values) / len(valid_values)) if valid_values else None

    @staticmethod
    def filter_valid_readings(readings, reading_attributes):
        return {attribute: [reading for reading in readings if getattr(reading, attribute) is not None]
                for attribute in reading_attributes}

    @staticmethod
    def find_extreme_values(readings_dict):
        """Find readings with the maximum value for each attribute.
        Args:
            readings_dict (dict[str, list[WeatherReading]]): Dictionary of
            attribute → list of readings.

        Returns:
            dict[str, WeatherReading | None]: Attribute → reading with the
            highest value or None if empty.
        """
        return {
            attribute: max(data, key=lambda reading: getattr(reading, attribute), default=None)
            for attribute, data in readings_dict.items()
        }

    def yearly_calculations(self, readings, year):
        yearly_readings = [reading for reading in readings if reading.date.year == year]
        if not yearly_readings:
            return None

        valid = self.filter_valid_readings(yearly_readings,
                                           ["max_temp", "min_temp", "mean_humidity"])
        extreme_values = self.find_extreme_values(valid)

        return {
            "highest_temperature": extreme_values["max_temp"],
            "lowest_temperature": extreme_values["min_temp"],
            "most_humid_day": extreme_values["mean_humidity"],
        }

    def monthly_calculations(self, readings, year, month):
        monthly_readings = [reading for reading in readings if reading.date.year == year
                            and reading.date.month == month]

        if not monthly_readings:
            return None

        return {
            "highest_average_temp": self.calculate_average(reading.max_temp for reading in monthly_readings),
            "lowest_average_temp": self.calculate_average(reading.min_temp for reading in monthly_readings),
            "average_mean_humidity": self.calculate_average(reading.mean_humidity for reading in monthly_readings),
        }
