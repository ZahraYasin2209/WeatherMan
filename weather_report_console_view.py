from weather_reading_helpers import (
    WeatherReadingFilter,
    WeatherReadingFormatter
)


class WeatherReportConsoleView:
    def __init__(self):
        self.readings_filter = WeatherReadingFilter()
        self.readings_formatter = WeatherReadingFormatter()

    @staticmethod
    def display_no_data(year=None, month=None):
        """
        Display a message indicating that no weather data is available.

        Args:
            year (int, optional): Year for which data is missing. Defaults to None.
            month (int, optional): Month for which data is missing (1–12). Defaults to None.

        Returns:
            None
        """
        print(f"No data available for {year}/{month:02d}"
              if year and month
              else "No data available.")

    @staticmethod
    def display_yearly_report(result):
        """
        Display the yearly weather report including highest temperature, lowest temperature,
        and highest mean humidity.

        Args:
            result (dict): Dictionary containing WeatherReading objects keyed by:
                "highest_temperature",
                "lowest_temperature",
                "highest_mean_humidity_day"
            Values may be None if data is missing.

        Returns:
            None
        """
        if not result:
            print("No data present for this year.")
            return

        labels = {
            "highest_temperature": ("Highest", "max_temp", "C"),
            "lowest_temperature": ("Lowest", "min_temp", "C"),
            "highest_mean_humidity_day": ("Humidity", "mean_humidity", "%"),
        }

        for key, (label, attribute, unit) in labels.items():
            weather_reading = result.get(key)

            yearly_weather_report = (
                f"{label}: {getattr(weather_reading, attribute)}{unit} on {weather_reading.date.strftime('%B %d')}"
                    if weather_reading
                    else f"No {label.lower()} data available for this year."
            )
            print(yearly_weather_report)

    def display_monthly_report(self, result, year=None, month=None):
        """
        Display the monthly weather report including highest average temperature,
        lowest average temperature, and average mean humidity.

        Args:
            result (dict | None): Dictionary containing monthly statistics with keys:
                "highest_average_temp" (int or float)
                "lowest_average_temp" (int or float)
                "average_mean_humidity" (int or float)
            Can be None if no data is available.
            year (int, optional): Year of the report. Used when displaying no data message.
            month (int, optional): Month of the report. Used when displaying no data message.

        Returns:
            None
        """
        if not result:
            return self.display_no_data(year, month)

        monthly_weather_report = (
            f"Highest Average: {result["highest_average_temp"]}C\n"
            f"Lowest Average: {result["lowest_average_temp"]}C\n"
            f"Average Mean Humidity: {result["average_mean_humidity"]}%"
        )
        print(monthly_weather_report)

    def display_chart(self, readings, year, month, horizontal=False):
        """
        Display a chart of temperatures for a given month.
        Uses temperature bars (vertical or horizontal) for visualization.

        Args:
            readings (list[WeatherReading]): List of WeatherReading objects.
            year (int): Year of the chart.
            month (int): Month of the chart (1–12).
            horizontal (bool, optional): Whether to display horizontal bars (True)
                                                 or vertical bars (False). Defaults to False.

        Returns:
            None
        """
        monthly_weather_readings = (self.readings_filter.
                                    get_sorted_readings_by_year_and_month(readings, year, month))

        if not monthly_weather_readings:
            return self.display_no_data(year, month)

        print(monthly_weather_readings[0].date.strftime("%B %Y"))

        for weather_reading in monthly_weather_readings:
            temp_bars = self.readings_formatter.format_temperature_bars(weather_reading, horizontal)
            if not temp_bars:
                continue
            for temp_chart_line in (temp_bars if isinstance(temp_bars, list) else [temp_bars]):
                print(temp_chart_line)
