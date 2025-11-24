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
            month (int, optional): Month for which data is missing. Defaults to None.

        Returns:
            None
        """
        print(
            f"No data available for {year}/{month:02d}"
            if year and month
            else "No data available."
        )

    def display_yearly_report(self, yearly_weather_report):
        """
        Display the yearly weather report including highest temperature, lowest temperature,
        and highest mean humidity.

        Args:
            yearly_weather_report (list[dict]): A list of dictionaries, each containing WeatherReading data with keys:
                "highest_temperature"
                "lowest_temperature"
                "highest_mean_humidity_day"
            Values may be None if data is missing.

        Returns:
            None
        """
        for weather_report in yearly_weather_report:
            print(weather_report)

    @staticmethod
    def display_monthly_report(monthly_statistics):
        """
        Display the monthly weather report including highest average temperature,
        lowest average temperature, and average mean humidity.

        Args:
            monthly_statistics (dict | None): Dictionary containing monthly statistics with keys:
                "highest_average_temp" (int or float)
                "lowest_average_temp" (int or float)
                "average_mean_humidity" (int or float)
        Returns:
            None
        """
        monthly_weather_report = (
            f"Highest Average: {monthly_statistics["highest_average_temp"]}C\n"
            f"Lowest Average: {monthly_statistics["lowest_average_temp"]}C\n"
            f"Average Mean Humidity: {monthly_statistics["average_mean_humidity"]}%"
        )
        print(monthly_weather_report)

    def display_temp_chart(self, formatted_temp_bars):
        """
        Display a formatted temperature chart for a month.

        Args:
            formatted_temp_bars (list[str]): A list of strings, each representing a line in the
            temperature chart, either vertical or horizontal.

        Returns:
            None
        """
        for temp_bar in formatted_temp_bars:
            print(temp_bar)

    def display_weather_report(
            self, weather_report_display_method, weather_report_data, year=None, month=None
    ):
        """
        Function to display the data (yearly, monthly, or charts).
        It checks if the data exists and displays it or calls display_no_data function.

        Args:
            weather_report_display_method (Callable): A function that takes `weather_report_data`
                and displays it (e.g., display_yearly_report, display_monthly_report, or display_temp_chart).
            weather_report_data (dict | list): The weather data to display.
            year (int, optional): Year for the report or chart. Defaults to None.
            month (int, optional): Month for the report or chart. Defaults to None.
        """

        if weather_report_data and weather_report_display_method:
            weather_report_display_method(weather_report_data)
        else:
            self.display_no_data(year, month)
