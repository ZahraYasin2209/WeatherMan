from constants import (
    BLUE,
    PURPLE,
    RED,
    RESET,
)


class WeatherReport:
    @staticmethod
    def display_no_data(year=None, month=None):
        print(f"No data available for {year}/{month:02d}"
              if year and month
              else "No data available.")

    @staticmethod
    def filter_sort_readings(readings, year, month):
        """Filter readings to include only those where specified attributes are not None.

        Args:
            readings (list[WeatherReading]): List of readings.
            year (int): Year.
            month (int): Month.

        Returns:
            dict[str, list[WeatherReading]]: Dictionary mapping attribute -> filtered readings.
        """
        return sorted(
            [reading for reading in readings if reading.date.year == year
             and reading.date.month == month], key=lambda reading: reading.date
        )

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

        day= f"{reading.date.day:02d}"

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

    @staticmethod
    def print_yearly_report(result):
        if not result:
            print("No data present for this year.")
            return

        labels = {
            "highest_temperature": ("Highest", "max_temp", "C"),
            "lowest_temperature": ("Lowest", "min_temp", "C"),
            "highest_mean_humidity_day": ("Humidity", "mean_humidity", "%"),
        }

        for key, (label, attribute, unit) in labels.items():
            reading = result.get(key)
            msg = (
                f"{label}: {getattr(reading, attribute)}{unit} on {reading.date.strftime('%B %d')}"
                if reading else f"No {label.lower()} data available for this year."
            )
            print(msg)

    def print_monthly_report(self, result, year=None, month=None):
        if not result:
            return self.display_no_data(year, month)

        print(
            f"Highest Average: {result['highest_average_temp']}C\n"
            f"Lowest Average: {result['lowest_average_temp']}C\n"
            f"Average Mean Humidity: {result['average_mean_humidity']}%"
        )

    def display_chart(self, readings, year, month, horizontal=False):
        monthly_readings = self.filter_sort_readings(readings, year, month)

        if not monthly_readings:
            return self.display_no_data(year, month)

        print(monthly_readings[0].date.strftime("%B %Y"))

        for reading in monthly_readings:
            bars = self.temperature_bars(reading, horizontal)
            if not bars:
                continue

            for line in (bars if isinstance(bars, list) else [bars]):
                print(line)
