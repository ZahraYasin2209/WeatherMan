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

    @staticmethod
    def display_yearly_report(yearly_statistics):
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
        weather_attribute_labels = {
            "highest_temperature": ("Highest", "max_temp", "C"),
            "lowest_temperature": ("Lowest", "min_temp", "C"),
            "highest_mean_humidity_day": ("Humidity", "mean_humidity", "%"),
        }

        for weather_attribute_key, weather_attribute_values in weather_attribute_labels.items():
            weather_attribute_label, weather_attribute, weather_unit_of_measurement = (
                weather_attribute_values
            )

            weather_reading = yearly_statistics.get(weather_attribute_key)

            if not weather_reading:
                continue

            weather_reading_measurement = getattr(weather_reading, weather_attribute, None)

            yearly_weather_report = (
                f"{weather_attribute_label}: {weather_reading_measurement}{weather_unit_of_measurement} "
                f"on {weather_reading.date.strftime("%B %d")}"
            )

            print(yearly_weather_report)

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
        Display a chart of temperatures for a given month.
        Uses temperature bars (vertical or horizontal) for visualization.

        Args:
            monthly_weather_readings (list[WeatherReading]):
                List of WeatherReading objects containing temperature data.
            horizontal (bool, optional): Whether to display horizontal bars (True)  or vertical bars (False).

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
            "chart": lambda data: self.display_temp_chart(data, horizontal)
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

        Returns:
            None
        """
        weather_report_display_method = self.get_weather_data_display_method(weather_data_category, horizontal)

        if weather_report_data and weather_report_display_method:
            weather_report_display_method(weather_report_data)
        else:
            self.display_no_data(year, month)
