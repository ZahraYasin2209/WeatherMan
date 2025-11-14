from constants import (
    BLUE,
    PURPLE,
    RED,
    RESET,
)


class WeatherReadingFilter:
    @staticmethod
    def filter_and_sort_readings(readings, year, month):
        """Filter readings to include only those where specified attributes are not None.

        Args:
             readings (list[WeatherReading]): List of weather reading objects.
             year (int): The year to filter by.
             month (int): The month to filter by (1–12).

        Returns:
            list[WeatherReading]: A list of WeatherReading objects that match
            the given year and month, sorted by date.
        """
        return sorted(
            [reading for reading in readings if reading.date.year == year
             and reading.date.month == month], key=lambda reading: reading.date
        )

    @staticmethod
    def filter_valid_readings(weather_readings, weather_attributes):
        return {weather_attribute: [reading for reading in weather_readings
                                    if getattr(reading, weather_attribute) is not None]
                for weather_attribute in weather_attributes}

    @staticmethod
    def filter_readings_by_year_and_month(weather_readings, year, month=None):
        return [reading for reading in weather_readings if reading.date.year == year and
                (month is None or reading.date.month == month)]


class WeatherReadingFormatter:
    @staticmethod
    def temperature_bars(reading, horizontal=False):
        """Generate temperature bar(s) for a single reading.

        Args:
            reading (WeatherReading): The weather reading.
            horizontal (bool): If True, return a horizontal bar format.

        Returns:
            str | list[str] | None: Formatted bar(s) or None if data missing.
        """
        if reading.max_temp is None or reading.min_temp is None:
            return None

        day = f"{reading.date.day:02d}"

        min_temp_bar = f"{BLUE}{'+' * reading.min_temp}"
        max_temp_bar = f"{RED}{'+' * reading.max_temp}"
        temp_values = f"{PURPLE} {reading.min_temp}C - {reading.max_temp}C {RESET}"

        return (
            f"{day} {min_temp_bar}+{max_temp_bar}{temp_values}" if horizontal else
            [
                f"{day} {max_temp_bar} {PURPLE}{reading.max_temp}C {RESET}",
                f"{day} {min_temp_bar} {PURPLE}{reading.min_temp}C {RESET}"
            ]
        )
