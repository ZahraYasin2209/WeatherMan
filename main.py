import argparse

from calculations import WeatherCalculator
from constants import DIRECTORY_PATH
from parser import WeatherDataParser
from reports import WeatherReport


class WeatherMan:
    def __init__(self):
        self.parser = WeatherDataParser()
        self.calculator = WeatherCalculator()
        self.report = WeatherReport()

    def run(self):
        parser = argparse.ArgumentParser(description="WeatherMan Project")

        parser.add_argument(
            "-e", "--yearly",
            type=int,
            nargs='+',
            help="Generate yearly reports. Provide YEAR(s)."
        )

        parser.add_argument(
            "-a", "--monthly",
            type=str,
            nargs='+',
            help="Generate monthly averages. Provide YEAR(s)/MONTH(s) (e.g: 2006/3)."
        )

        parser.add_argument(
            "-c", "--chart",
            type=str,
            nargs='+',
            help="Generate vertical monthly charts. Provide YEAR(s)/MONTH(s)."
        )

        parser.add_argument(
            "-b", "--hchart",
            type=str,
            nargs='+',
            help="Generate horizontal monthly charts. Provide YEAR/MONTH."
        )

        args = parser.parse_args()

        readings = self.parser.parse_directory(DIRECTORY_PATH)

        if args.yearly:
            for year in args.yearly:
                yearly_report = self.calculator.yearly_calculations(readings, year)
                self.report.print_yearly_report(yearly_report)

        if args.monthly:
            for option in args.monthly:
                try:
                    year, month = map(int, option.split("/"))
                    monthly_report = self.calculator.monthly_calculations(readings, year, month)
                    self.report.print_monthly_report(monthly_report, year, month)
                except ValueError:
                    print(f"Invalid format for monthly report: {option}. Use YEAR/MONTH")

        for chart_args, horizontal in [(args.chart, False), (args.hchart, True)]:
            for option in chart_args or []:
                try:
                    year, month = map(int, option.split("/"))
                    self.report.display_chart(readings, year, month, horizontal=horizontal)
                except ValueError:
                    print(f"Invalid format for chart: {option}. Use YEAR/MONTH")


if __name__ == "__main__":
    WeatherMan().run()
