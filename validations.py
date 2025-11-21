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

    def validate_yearly_weather_readings_by_attribute(self, yearly_weather_readings, weather_attributes):
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
