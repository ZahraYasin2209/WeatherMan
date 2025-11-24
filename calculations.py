from constants import (
    AVERAGE_DEFAULT_VALUE,
    ROUNDED_AVERAGE_PRECISION,
)


class WeatherCalculator:
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

    def calculate_monthly_averages(self, validated_attribute_values):
        """
        Calculate the average value for each weather attribute in a monthly dataset.

        Args:
            validated_attribute_values (dict[str, list[float | int]]):
                A dictionary mapping attribute keys (e.g., "highest_average_temp",
                "lowest_average_temp", "average_mean_humidity") to lists of validated
                numeric values for that attribute.

        Returns:
            dict[str, float]: A dictionary mapping each attribute key to its calculated
            average value, rounded according to WeatherCalculator's logic.
            """
        return {
            monthly_average_key: self.calculate_average(validated_values)
            for monthly_average_key, validated_values in validated_attribute_values.items()
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
