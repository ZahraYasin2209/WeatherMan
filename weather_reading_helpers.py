from constants import (
    BLUE,
    PURPLE,
    RED,
    RESET,
    WEATHER_ATTRIBUTES,
    YEARLY_ATTRIBUTE_MAP
)


class WeatherReadingFilter:
    @staticmethod
    def get_sorted_readings_by_year_and_month(readings, year, month):
        """
        Return weather readings for a given year and month, sorted by date.

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
        return {
            weather_attribute: [
                reading
                for reading in weather_readings
                if getattr(reading, weather_attribute)
            ]
            for weather_attribute in weather_attributes
        }

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

    def get_yearly_weather_readings(self, weather_readings, year):
        """
        Return all readings for a specified year.

        Args:
            weather_readings (list[WeatherReading]): List of weather reading objects.
            year (int): Year to filter by.

        Returns:
            list[WeatherReading]: List of readings for the specified year.
        """
        return self.get_readings_by_year_and_month(weather_readings, year)

    @staticmethod
    def get_all_attributes_with_valid_readings(valid_weather_readings):
        """
        Check if all weather attributes have valid (non-empty) readings.

        Args:
            valid_weather_readings (dict[str, list[WeatherReading]]):
            Dictionary of readings by attribute.

        Returns:
            bool: True if all attributes have at least one valid reading, False otherwise.
        """
        return (
            all(valid_weather_readings[weather_attribute]
                for weather_attribute in WEATHER_ATTRIBUTES)
        )

    @staticmethod
    def get_yearly_max_weather_values(max_values_per_attribute):
        """
        Map max values of attributes to yearly statistics keys.

        Args:
            max_values_per_attribute (dict[str, WeatherReading]): Max reading per attribute.

        Returns:
            dict[str, WeatherReading]: Dictionary mapping yearly stat keys to readings.
        """
        return {
            yearly_stats_identifier: max_values_per_attribute.get(input_weather_attr)
            for input_weather_attr, yearly_stats_identifier in YEARLY_ATTRIBUTE_MAP.items()
        }

    @staticmethod
    def get_attribute_values(weather_readings, weather_attribute):
        """
        Extract non-None values for a specific attribute from readings.

        Args:
            weather_readings (list[WeatherReading]): List of weather reading objects.
            weather_attribute (str): Attribute name to extract (e.g., 'max_temp').

        Returns:
            list[float | int]: List of attribute values that are not None.
        """
        return [
            getattr(reading, weather_attribute)
            for reading in weather_readings
            if getattr(reading, weather_attribute)
        ]


class WeatherReadingFormatter:
    def format_yearly_weather_report(self, yearly_statistics):
        """
        Format yearly weather report as strings.

        Args:
            yearly_statistics (dict): Dictionary containing WeatherReading objects with keys:
                "highest_temperature"
                "lowest_temperature"
                "highest_mean_humidity_day"

        Returns:
            list[str]: List of formatted strings for the report.
        """
        weather_attribute_labels = {
            "highest_temperature": ("Highest", "max_temp", "C"),
            "lowest_temperature": ("Lowest", "min_temp", "C"),
            "highest_mean_humidity_day": ("Humidity", "mean_humidity", "%"),
        }

        yearly_weather_report = []
        for weather_attribute_key, weather_attribute_values in weather_attribute_labels.items():
            weather_attribute_label, weather_attribute, weather_unit_of_measurement = (
                weather_attribute_values
            )

            weather_reading = yearly_statistics.get(weather_attribute_key)

            if not weather_reading:
                    continue

            weather_reading_measurement = getattr(weather_reading, weather_attribute, None)

            yearly_weather_report.append(
                f"{weather_attribute_label}: {weather_reading_measurement}{weather_unit_of_measurement} "
                f"on {weather_reading.date.strftime("%B %d")}"
            )

        return yearly_weather_report

    @staticmethod
    def format_temperature_bars(weather_reading, horizontal=False):
        """
        Generate temperature bar(s) for a single reading.

        Args:
            weather_reading (WeatherReading): The weather reading.
            horizontal (bool): If True, return a horizontal bar format.

        Returns:
            str | list[str] | None: Formatted bar(s) or None if data missing.
        """
        temp_bars_formatter = None

        if weather_reading.max_temp and weather_reading.min_temp:
            day = f"{weather_reading.date.day:02d}"

            min_temp_bar = f"{BLUE}{'+' * max(0, weather_reading.min_temp)}"
            max_temp_bar = f"{RED}{'+' * max(0, weather_reading.max_temp)}"
            temp_values = f"{PURPLE} {weather_reading.min_temp}C - {weather_reading.max_temp}C {RESET}"

            temp_bars_formatter = (
                f"{day} {min_temp_bar}+{max_temp_bar}{temp_values}" if horizontal else
                [
                    f"{day} {max_temp_bar} {PURPLE}{weather_reading.max_temp}C {RESET}",
                    f"{day} {min_temp_bar} {PURPLE}{weather_reading.min_temp}C {RESET}"
                ]
            )

        return temp_bars_formatter

    def format_temp_chart(self, monthly_weather_readings, horizontal=False):
        """
        Prepare temperature chart lines for a month.

        Args:
            monthly_weather_readings (list[WeatherReading]): List of readings.
            horizontal (bool): Whether to format horizontal bars.

        Returns:
            list[str]: List of lines for printing.
        """
        temp_chart_lines = [monthly_weather_readings[0].date.strftime("%B %Y")]

        for reading in monthly_weather_readings:
            temp_bars = self.format_temperature_bars(reading, horizontal)
            if not temp_bars:
                continue

            temp_chart_lines.extend(
                temp_bars if isinstance(temp_bars, list) else [temp_bars]
            )

        return temp_chart_lines
