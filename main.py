import argparse

from calculations import WeatherCalculator
from constants import (
    DEFAULT_WEATHER_DIR_PATH,
    MONTHLY_ATTRIBUTE_MAP,
    WEATHER_ATTRIBUTES,
)
from parser import (
    InputDateParser,
    WeatherDataParser
)
from validations import WeatherReadingValidator
from weather_reading_helpers import (
    WeatherReadingFilter,
    WeatherReadingFormatter
)
from weather_report_console_view import WeatherReportConsoleView


class WeatherMan:
    def __init__(self):
        self.date_parser = InputDateParser()
        self.reading_filter = WeatherReadingFilter()
        self.reading_formatters = WeatherReadingFormatter()
        self.reading_validator = WeatherReadingValidator()
        self.report = WeatherReportConsoleView()
        self.weather_calculator = WeatherCalculator()
        self.weather_data_parser = WeatherDataParser()

    def run(self):
        """
        Parse Command-Line Arguments and execute requested weather reports or temperature charts.

        Command-line arguments supported:
            directory (str): Path to directory containing weather files.
            -e, --yearly YEAR [YEAR ...]: Generate yearly reports for given YEAR(s).
            -a, --monthly YEAR/MONTH [YEAR/MONTH ...]: Generate monthly averages.
            -c, --chart YEAR/MONTH [YEAR/MONTH ...]: Generate vertical monthly charts.
            -b, --hchart YEAR/MONTH [YEAR/MONTH ...]: Generate horizontal monthly charts.

        Behavior:
            Parses all CSV files in the specified directory.
            Generates and displays reports based on user CLI arguments.
            Validates YEAR/MONTH input formats and prints respective errors for invalid formats.

        Returns:
            Requested weather reports or temperature charts or Error messages.
        """
        parser = argparse.ArgumentParser(description="WeatherMan Project")

        parser.add_argument(
            "directory",
            nargs="?",
            default=DEFAULT_WEATHER_DIR_PATH,
            help="Weather directory containing weather data files."
        )

        parser.add_argument(
            "-e", "--yearly",
            type=int,
            nargs="+",
            help="Generate yearly reports. Provide YEAR(s)."
        )

        parser.add_argument(
            "-a", "--monthly",
            type=str,
            nargs="+",
            help="Generate monthly averages. Provide YEAR(s)/MONTH(s) (e.g: 2006/3)."
        )

        parser.add_argument(
            "-c", "--chart",
            type=str,
            nargs="+",
            help="Generate vertical monthly charts. Provide YEAR(s)/MONTH(s)."
        )

        parser.add_argument(
            "-b", "--hchart",
            type=str,
            nargs="+",
            help="Generate horizontal monthly charts. Provide YEAR/MONTH."
        )

        args = parser.parse_args()

        weather_readings = self.weather_data_parser.parse_directory_to_readings(args.directory)

        if args.yearly:
            for raw_year in args.yearly:
                try:
                    year = self.date_parser.parse_and_validate_year(raw_year)

                    yearly_weather_readings = self.reading_filter.get_readings_by_year_and_month(
                        weather_readings,
                        year
                    )

                    valid_weather_readings = self.reading_validator.validate_yearly_weather_readings_by_attribute(
                        yearly_weather_readings,
                        WEATHER_ATTRIBUTES
                    )

                    max_values_per_attribute = self.weather_calculator.find_max_reading_per_attribute(
                        valid_weather_readings
                    )

                    yearly_report = self.reading_filter.get_yearly_max_weather_values(
                        max_values_per_attribute
                    )

                    formatted_weather_report = self.reading_formatters.format_yearly_weather_report(
                        yearly_report
                    )

                    self.report.display_weather_report(
                        self.report.display_yearly_report,
                        formatted_weather_report,
                        year=year
                    )
                except ValueError as date_input_error:
                    print(date_input_error)

        if args.monthly:
            for raw_month in args.monthly:
                try:
                    year, month = self.date_parser.parse_and_validate_year_and_month(raw_month)

                    monthly_weather_readings = self.reading_filter.get_sorted_readings_by_year_and_month(
                        weather_readings,
                        year,
                        month
                    )

                    if monthly_weather_readings:
                        validated_values = self.reading_validator.validate_monthly_weather_readings(
                            monthly_weather_readings,
                            MONTHLY_ATTRIBUTE_MAP
                        )

                        monthly_averages = self.weather_calculator.calculate_monthly_averages(
                            validated_values
                        )

                        self.report.display_weather_report(
                            self.report.display_monthly_report,
                            monthly_averages,
                            year=year,
                            month=month
                        )
                except ValueError as date_input_error:
                    print(date_input_error)

        for chart_args, horizontal in [(args.chart, False), (args.hchart, True)]:
            for monthly_weather_chart in chart_args or []:
                try:
                    year, month = self.date_parser.parse_and_validate_year_and_month(monthly_weather_chart)

                    monthly_weather_readings = self.reading_filter.get_sorted_readings_by_year_and_month(
                        weather_readings,
                        year,
                        month
                    )

                    if monthly_weather_readings:
                        formatted_temp_bars = self.reading_formatters.format_temp_chart(
                            monthly_weather_readings, horizontal
                        )

                        self.report.display_weather_report(
                            self.report.display_temp_chart,
                            formatted_temp_bars,
                            year=year,
                            month=month
                        )
                except ValueError as date_input_error:
                    print(date_input_error)


if __name__ == "__main__":
    WeatherMan().run()
