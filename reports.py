RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"


def print_yearly_report(result):
    if not result or (not result.get('highest') and not result.get('lowest')
                      and not result.get('humid')):
        print("No data present for this year")
        return

    if result['highest']:
        print(f"Highest: {result['highest'].max_temp}C on {result['highest'].
          date.strftime('%B %d')}")
    else:
        print("No highest temperature data available for this year.")

    if result['lowest']:
        print(f"Lowest: {result['lowest'].min_temp}C on {result['lowest'].
          date.strftime('%B %d')}")
    else:
        print("No lowest temperature data available for this year.")

    if result['humid']:
        print(f"Humidity: {result['humid'].mean_humidity}% on {result['humid'].
          date.strftime('%B %d')}")
    else:
        print("No humidity data available for this year.")


def print_monthly_report(result, year=None, month=None):
    if not result:
        if year and month:
            print(f"No data available for {year}/{month:02d}")
        else:
            print("No data available for this month")
        return

    print(f"Highest Average: {result.get('highest_average_temp', 'N/A')}C")
    print(f"Lowest Average: {result.get('lowest_average_temp', 'N/A')}C")
    print(f"Average Mean Humidity: {result.get('average_mean_humidity', 'N/A')}%")


""" Filter and sort readings for given year and month """
def filter_sort_readings(readings, year, month):
    return sorted(
        [reading for reading in readings if reading.date.year == year and reading.date.month == month],
        key=lambda reading: reading.date
    )


def temperature_bars(reading, horizontal=False):
    if reading.max_temp is None or reading.min_temp is None:
        return None
    day = f"{reading.date.day:02d}"

    if horizontal:
        return (
            f"{day} {BLUE}{'+' * reading.min_temp}+{RED}{'+' * reading.max_temp} {
            PURPLE}{reading.min_temp}C - {reading.max_temp}C {RESET}"
        )
    else:
        return (
            f"{day} {RED}{'+' * reading.max_temp} {PURPLE}{reading.max_temp}C {RESET}", \
            f"{day} {BLUE}{'+' * reading.min_temp} {PURPLE}{reading.min_temp}C {RESET}"
        )


def monthly_chart(readings, year, month):
    month_data = filter_sort_readings(readings, year, month)

    if not month_data:
        print("No data present for this month")
        return

    month_name = month_data[0].date.strftime("%B %Y") if month_data else "Month not exists"
    print(f"{month_name}")

    for reading in month_data:
        formatted_bars = temperature_bars(reading, horizontal=False)
        if formatted_bars:
            print(formatted_bars[0])
            print(formatted_bars[1])


def horizontal_monthly_chart(readings, year, month):
    month_data = filter_sort_readings(readings, year, month)

    if not month_data:
        print("No data present for this month")
        return

    month_name = month_data[0].date.strftime("%B %Y") if month_data else "Month not exists"
    print(f"{month_name}")

    for reading in month_data:
        formatted_bars = temperature_bars(reading, horizontal=True)
        if formatted_bars:
            print(formatted_bars)
