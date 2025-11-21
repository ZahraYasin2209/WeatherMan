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
            yearly_statistics (dict): Dictionary containing WeatherReading objects having keys:
                "highest_temperature",
                "lowest_temperature",
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

    def display_temp_chart(self, monthly_weather_readings, horizontal=False):
        """
        Print the temperature chart for a given month.

        Args:
            monthly_weather_readings (list[WeatherReading]): List of readings.
            horizontal (bool): If True, display horizontal bars.
        """
        weather_temp_bars = self.readings_formatter.format_temp_chart(monthly_weather_readings, horizontal)

        for temp_bar in weather_temp_bars:
            print(temp_bar)

    def get_weather_data_display_method(self, weather_data_category, horizontal=False):
        """
        Returns the appropriate function to display weather data based on the category.

        Args:
            weather_data_category (str): Type of weather data. Expected values:
                - "yearly": for yearly weather reports
                - "monthly": for monthly weather reports
                - "chart": for temperature charts (horizontal or vertical)
            horizontal (bool, optional): If True and the category is "chart", the
                returned function will display the chart horizontally. Defaults to False.

        Returns:
            Callable[[dict | list], None]: A callable that takes the weather data
            as input and displays it. Returns None if the category is invalid.
        """
        weather_report_display_methods = {
            "yearly": self.display_yearly_report,
            "monthly": self.display_monthly_report,
            "chart": lambda weather_data: self.display_temp_chart(weather_data, horizontal)
        }

        return weather_report_display_methods.get(weather_data_category)

    def display_weather_report(
            self, weather_data_category, weather_report_data, year=None, month=None, horizontal=False
    ):
        """
        Function to display the data (yearly, monthly, or charts).
        It checks if the data exists and displays it or calls display_no_data function.

        Args:
            weather_data_category (str): Type of data - "yearly", "monthly", or "chart".
            weather_report_data (dict | list): The data to display.
            year (int, optional): Year for the report or chart. Defaults to None.
            month (int, optional): Month for the report or chart. Defaults to None.
            horizontal (bool, optional): If True, display horizontal chart. Defaults to False.
        """
        weather_report_display_method = self.get_weather_data_display_method(
            weather_data_category, horizontal
        )

        if weather_report_data and weather_report_display_method:
            weather_report_display_method(weather_report_data)
        else:
            self.display_no_data(year, month)
