from weather_reading_utils import (
    WeatherReadingFilter,
    WeatherReadingFormatter
)


class WeatherReportConsoleView:
    def __init__(self):
        self.readings_filter = WeatherReadingFilter()
        self.readings_formatter = WeatherReadingFormatter()

    @staticmethod
    def display_no_data(year=None, month=None):
        print(f"No data available for {year}/{month:02d}"
              if year and month
              else "No data available.")

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
        monthly_readings = self.readings_filter.filter_and_sort_readings(readings, year, month)

        if not monthly_readings:
            return self.display_no_data(year, month)

        print(monthly_readings[0].date.strftime("%B %Y"))

        for reading in monthly_readings:
            bars = self.readings_formatter.temperature_bars(reading, horizontal)
            if not bars:
                continue
            for line in (bars if isinstance(bars, list) else [bars]):
                print(line)
