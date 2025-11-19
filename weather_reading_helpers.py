from constants import (
    BLUE,
    PURPLE,
    RED,
    RESET,
)


class WeatherReadingFilter:
    @staticmethod
    def get_sorted_readings_by_year_and_month(readings, year, month):
        """
        Filter readings to include only those where specified attributes are not None.

        Args:
             readings (list[WeatherReading]): List of weather reading objects.
             year (int): The year to filter by.
             month (int): The month to filter by (1–12).

        Returns:
            list[WeatherReading]: A list of WeatherReading objects that match
            the given year and month, sorted by date.
        """
        return sorted(
            [
                reading
                for reading in readings
                if reading.date.year == year and reading.date.month == month
            ],
            key=lambda reading: reading.date
        )

    @staticmethod
    def get_valid_readings_by_attribute(weather_readings, weather_attributes):
        """
        Filter readings to include only those where specified attributes are not None.

        Args:
            weather_readings (list[WeatherReading]): List of weather reading objects.
            weather_attributes (list[str]): List of attribute names to filter on
                (e.g., ["max_temp", "min_temp", "mean_humidity"]).

        Returns:
            dict[str, list[WeatherReading]]: Dictionary mapping each attribute name to a list of readings
            where that attribute is not None.
        """

        filtered_valid_readings_by_attribute = {}

        for weather_attribute in weather_attributes:
            valid_weather_readings = []

            for reading in weather_readings:
                attribute_value = getattr(reading, weather_attribute)

                if attribute_value:
                    valid_weather_readings.append(reading)

            filtered_valid_readings_by_attribute[weather_attribute] = valid_weather_readings

        return filtered_valid_readings_by_attribute

    @staticmethod
    def get_readings_by_year_and_month(weather_readings, year, month=None):
        """
        Filter readings by year and optionally by month.

        Args:
            weather_readings (list[WeatherReading]): List of weather reading objects.
            year (int): Year to filter by.
            month (int | None, optional): Month to filter by (1–12). If None, returns all readings for the year.

        Returns:
            list[WeatherReading]: List of readings matching the specified year and, if provided, month.
        """
        return [
            reading
            for reading in weather_readings
            if reading.date.year == year and (month is None or reading.date.month == month)
        ]


class WeatherReadingFormatter:
    @staticmethod
    def format_temperature_bars(reading, horizontal=False):
        """
        Generate temperature bar(s) for a single reading.

        Args:
            reading (WeatherReading): The weather reading.
            horizontal (bool): If True, return a horizontal bar format.

        Returns:
            str | list[str] | None: Formatted bar(s) or None if data missing.
        """
        temp_bars_formatter = None

        if reading.max_temp and reading.min_temp:
            day = f"{reading.date.day:02d}"

            min_temp_bar = f"{BLUE}{'+' * max(0, reading.min_temp)}"
            max_temp_bar = f"{RED}{'+' * max(0, reading.max_temp)}"
            temp_values = f"{PURPLE} {reading.min_temp}C - {reading.max_temp}C {RESET}"

            temp_bars_formatter = (
                f"{day} {min_temp_bar}+{max_temp_bar}{temp_values}" if horizontal else
                [
                    f"{day} {max_temp_bar} {PURPLE}{reading.max_temp}C {RESET}",
                    f"{day} {min_temp_bar} {PURPLE}{reading.min_temp}C {RESET}"
                ]
            )

        return temp_bars_formatter
