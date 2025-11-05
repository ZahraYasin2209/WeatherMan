import sys
from parser_module import parse_weather_files
from calculations_module import yearly_calculations
from calculations_module import monthly_average
from reports import (horizontal_monthly_chart,
                     print_monthly_report,
                     print_yearly_report,
                     monthly_chart)


def main():
    if len(sys.argv) < 4:
        print("INVALID ARGUMENT")
        print("PLEASE PROVIDE ACCURATE ARGUMENTS")
        print("SAMPLE: weatherman.py //path_to_directory -e|-a|-c|-b YEAR[/MONTH]")
        return

    directory = sys.argv[1]
    readings = parse_weather_files(directory)

    #Handling multiple reports
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "-e":         # For Yearly temperature report
            year = int(args[i+1])
            result = yearly_calculations(readings, year)
            print_yearly_report(result)
            i += 2
        elif args[i] == "-a":       # For Monthly temperature
            year, month = map(int, args[i+1].split("/"))
            result = monthly_average(readings, year, month)
            print_monthly_report(result)
            i += 2
        elif args[i] == "-c":       # For barchart
            year, month = map(int, args[i+1].split("/"))
            monthly_chart(readings, year, month)
            i += 2
        elif args[i] == "-b":       # For horizontal bar chart
            year, month = map(int, args[i+1].split("/"))
            horizontal_monthly_chart(readings, year, month)
            i += 2
        elif args[i] not in ["-e", "-a", "-c", "-b"]:
            print("INVALID ARGUMENT")
            return
        else:
            i += 1


if __name__ == "__main__":
    main()



