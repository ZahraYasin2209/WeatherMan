import argparse

from calculations import WeatherCalculator
from constants import DEFAULT_WEATHER_DIR_PATH
from parser import WeatherDataParser
from weather_report_console_view import WeatherReportConsoleView
from weather_reading_helpers import WeatherReadingFilter


class WeatherMan:
    def __init__(self):
        self.parser = WeatherDataParser()
        self.calculator = WeatherCalculator()
        self.report = WeatherReportConsoleView()
        self.readings = WeatherReadingFilter()

    def run(self):
        """
        Parse Command-Line Arguments and execute requested weather reports or temperature charts.

        Command-line arguments supported:
            directory (str, optional): Path to directory containing weather files.
                                            Default set to DEFAULT_WEATHER_DIR_PATH.
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

        directory = args.directory
        weather_readings = self.parser.parse_directory_to_readings(directory)

        if args.yearly:
            for year in args.yearly:
                try:
                    yearly_report = self.calculator.calculate_yearly_weather_statistics(
                        weather_readings, year
                    )

                    if yearly_report:
                        self.report.display_yearly_report(yearly_report)
                    else:
                        self.report.display_no_data(year)
                except ValueError:
                    print(f"Invalid format for monthly report: '{year}'. Please use YEAR/MONTH Format")

        if args.monthly:
            for option in args.monthly:
                try:
                    year, month = map(int, option.split("/"))

                    monthly_report = self.calculator.calculate_monthly_weather_statistics(
                        weather_readings, year, month
                    )

                    if monthly_report:
                        self.report.display_monthly_report(monthly_report, year, month)
                    else:
                        self.report.display_no_data(year, month)
                except ValueError:
                    print(f"Invalid format for monthly report: {option}. Please use YEAR/MONTH Format")

        for chart_args, horizontal in [(args.chart, False), (args.hchart, True)]:
            for option in chart_args or []:
                try:
                    year, month = map(int, option.split("/"))

                    monthly_weather_readings = self.readings.get_sorted_readings_by_year_and_month(
                        weather_readings, year, month
                    )

                    if not monthly_weather_readings:
                        self.report.display_no_data(year, month)
                    else:
                        self.report.display_temp_chart(monthly_weather_readings, horizontal=horizontal)
                except ValueError:
                    print(f"Invalid format for chart: {option}. Please use YEAR/MONTH Format")


if __name__ == "__main__":
    WeatherMan().run()
