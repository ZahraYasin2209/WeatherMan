import argparse

from constants import DIRECTORY_PATH
from calculations import WeatherCalculator
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
            help="Generate yearly report. Provide YEAR.")

        parser.add_argument(
            "-a", "--monthly",
            type=str,
            help="Generate monthly averages. Provide YEAR/MONTH.")

        parser.add_argument(
            "-c", "--chart",
            type=str,
            help="Generate vertical monthly chart. Provide YEAR/MONTH.")

        parser.add_argument(
            "-b", "--hchart",
            type=str,
            help="Generate horizontal monthly chart. Provide YEAR/MONTH.")

        args = parser.parse_args()

        readings = self.parser.parse_directory(DIRECTORY_PATH)

        if args.yearly:
            result = self.calculator.yearly_calculations(readings, args.yearly)
            self.report.print_yearly_report(result)

        if args.monthly:
            try:
                year, month = map(int, args.monthly.split("/"))
                result = self.calculator.monthly_calculations(readings, year, month)
                self.report.print_monthly_report(result, year, month)
            except ValueError:
                print("Month requires format YEAR/MONTH (e.g: 2006/5)")

        if args.chart or args.hchart:
            option = args.chart or args.hchart
            try:
                year, month = map(int, option.split("/"))
                horizontal = bool(args.hchart)
                self.report.display_chart(readings, year, month, horizontal=horizontal)
            except ValueError:
                print("Chart requires format YEAR/MONTH (e.g: 2006/5)")


if __name__ == "__main__":
    WeatherMan().run()
