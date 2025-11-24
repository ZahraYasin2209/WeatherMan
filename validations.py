from weather_reading_helpers import WeatherReadingFilter


class WeatherReadingValidator:
    def __init__(self):
        self.readings = WeatherReadingFilter()

    @staticmethod
    def validate_weather_readings(weather_readings):
        """
        Filter out invalid readings (None or non-numeric).

        Args:
            weather_readings (list[float | int | None]): List of readings.

        Returns:
            list[float | int]: List containing only valid readings.
        """
        return [
            reading
            for reading in weather_readings
            if reading
        ]

    def validate_yearly_weather_readings_by_attribute(
            self, yearly_weather_readings, weather_attributes
    ):
        """
        Validate yearly weather readings for specified attributes.

        Args:
            yearly_weather_readings (list[WeatherReading]): List of yearly weather readings.
            weather_attributes (list[str]): List of attributes to validate (e.g., temperature, humidity).

        Returns:
            dict[str, list[WeatherReading]]: Dictionary of attributes mapping to valid weather readings.
        """
        return self.readings.get_valid_readings_by_attribute(
            yearly_weather_readings,
            weather_attributes
        )

    def extract_and_validate_attribute(self, weather_readings, weather_attribute):
        """
        Extract the values of a specific weather attribute from a list of readings and validate them
        by removing None or invalid entries.

        Args:
            weather_readings (list[WeatherReading]): List of WeatherReading objects
                from which the attribute values will be extracted.
            weather_attribute (str): The name of the weather attribute to extract
                (e.g., "max_temp", "min_temp", "mean_humidity").

        Returns:
            list[float | int]: A list of valid values for the specified attribute,
            with None or invalid entries removed.
        """
        extracted_attribute_values = self.readings.get_attribute_values(
            weather_readings, weather_attribute
        )

        return self.validate_weather_readings(extracted_attribute_values)

    def validate_monthly_weather_readings(self, monthly_weather_readings, weather_attributes):
        """
        Validate weather attribute values for a monthly dataset.

        Args:
            monthly_weather_readings (list[WeatherReading]): List of WeatherReading objects
            weather_attributes (dict[str, str]): Dictionary mapping attribute keys (e.g., "max_temp", "min_temp",
            "mean_humidity") to their corresponding attribute names in WeatherReading objects.

        Returns:
            dict[str, list[float | int]]: Dictionary mapping each attribute key to a list
            of validated numeric values extracted from the monthly readings.
        """
        validated_attribute_values_per_key  = {}

        for weather_attribute_key, weather_attribute_name in weather_attributes.items():
            extracted_attribute_values = self.readings.get_attribute_values(
                monthly_weather_readings, weather_attribute_name
            )

            validated_attribute_values_per_key[weather_attribute_key] = self.validate_weather_readings(
                extracted_attribute_values
            )

        return validated_attribute_values_per_key
