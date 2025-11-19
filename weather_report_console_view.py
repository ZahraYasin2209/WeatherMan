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
        print(
            f"No data available for {year}/{month:02d}"
            if year and month
            else "No data available."
        )


    def display_yearly_report(self, yearly_statistics):
        """
        Display the yearly weather report including highest temperature, lowest temperature,
        and highest mean humidity.

        Args:
            yearly_statistics (dict): Dictionary containing WeatherReading objects keyed by:
                "highest_temperature",
                "lowest_temperature",
                "highest_mean_humidity_day"
            Values may be None if data is missing.

        Returns:
            None
        """
        weather_attribute_labels = {
            "highest_temperature": ("Highest", "max_temp", "C"),
            "lowest_temperature": ("Lowest", "min_temp", "C"),
            "highest_mean_humidity_day": ("Humidity", "mean_humidity", "%"),
        }

        for weather_attribute_key, (
                weather_attribute_label, weather_attribute, weather_unit_of_measurement
        ) in weather_attribute_labels.items():
            weather_reading = yearly_statistics.get(weather_attribute_key)

            if not weather_reading:
                continue

            weather_reading_measurement = getattr(weather_reading, weather_attribute, None)

            if weather_reading_measurement:
                weather_report_date = weather_reading.date.strftime("%B %d")

                yearly_weather_report = (
                    f"{weather_attribute_label}: {weather_reading_measurement}{weather_unit_of_measurement} "
                    f"on {weather_report_date}"
                )

                print(yearly_weather_report)

    def display_monthly_report(self, monthly_statistics, year=None, month=None):
        """
        Display the monthly weather report including highest average temperature,
        lowest average temperature, and average mean humidity.

        Args:
            monthly_statistics (dict | None): Dictionary containing monthly statistics with keys:
                "highest_average_temp" (int or float)
                "lowest_average_temp" (int or float)
                "average_mean_humidity" (int or float)
            Can be None if no data is available.
            year (int, optional): Year of the report. Used when displaying no data message.
            month (int, optional): Month of the report. Used when displaying no data message.

        Returns:
            None
        """

        monthly_weather_report = (
            f"Highest Average: {monthly_statistics["highest_average_temp"]}C\n"
            f"Lowest Average: {monthly_statistics["lowest_average_temp"]}C\n"
            f"Average Mean Humidity: {monthly_statistics["average_mean_humidity"]}%"
        )
        print(monthly_weather_report)

    def display_temp_chart(self, monthly_weather_readings, horizontal=False):
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
        print(monthly_weather_readings[0].date.strftime("%B %Y"))

        for weather_reading in monthly_weather_readings:
            temp_bars = self.readings_formatter.format_temperature_bars(
                weather_reading,
                horizontal
            )

            if not temp_bars:
                continue
            for temp_chart_line in (temp_bars if isinstance(temp_bars, list) else [temp_bars]):
                print(temp_chart_line)
