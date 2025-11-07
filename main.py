import argparse

from parser import parse_weather_files
from calculations import yearly_calculations, monthly_average
from reports import (
    horizontal_monthly_chart,
    print_monthly_report,
    print_yearly_report,
    monthly_chart,
)
from constants import DIRECTORY_PATH


def main():
    parser = argparse.ArgumentParser(description="WeatherMan Project")

    parser.add_argument(
        "-e", "--yearly",
        type=int,
        help="Generate an yearly report. Provide YEAR."
    )

    parser.add_argument(
        "-a", "--monthly",
        type=str,
        help="Generate a monthly report. Provide YEAR/MONTH."
    )

    parser.add_argument(
        "-c", "--chart",
        type=str,
        help="Generate a monthly chart. Provide YEAR/MONTH."
    )

    parser.add_argument(
        "-b", "--hchart",
        type=str,
        help="Generate a horizontal monthly chart. Provide YEAR/MONTH."
    )

    args = parser.parse_args()
    readings = parse_weather_files(DIRECTORY_PATH)

    if args.yearly:
        result = yearly_calculations(readings, args.yearly)
        print_yearly_report(result)

    if args.monthly:
        try:
            year, month = map(int, args.monthly.split("/"))
        except ValueError:
            print("Month requires format YEAR/MONTH (e.g: 2006/5)")
            return

        if month < 1 or month > 12:
            print(f"Invalid month: {month}. Month should be between 1 and 12.")
            return
        result = monthly_average(readings, year, month)
        print_monthly_report(result, year, month)

    if args.chart:
        try:
            year, month = map(int, args.chart.split("/"))
        except ValueError:
            print("Chart requires format YEAR/MONTH (e.g: 2006/5)")
            return

        if month < 1 or month > 12:
            print(f"Invalid month: {month}. Month should be between 1 and 12.")
            return
        monthly_chart(readings, year, month)

    if args.hchart:
        try:
            year, month = map(int, args.hchart.split("/"))
        except ValueError:
            print("Horizontal Chart requires format YEAR/MONTH (e.g: 2006/5)")
            return

        if month < 1 or month > 12:
            print(f"Invalid month: {month}. Month should be between 1 and 12.")
            return
        horizontal_monthly_chart(readings, year, month)


if __name__ == "__main__":
    main()
