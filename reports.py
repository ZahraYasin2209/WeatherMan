RED = "\033[91m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
RESET = "\033[0m"


def print_yearly_report(result):
    if not result:
        print("No data present for this year")
        return

    print(f"Highest: {result['highest'].max_temp}C on {result['highest'].
          date.strftime('%B %d')}")             # Highest temp in year
    print(f"Lowest: {result['lowest'].min_temp}C on {result['lowest'].
          date.strftime('%B %d')}")             # Lowest temp in year
    print(f"Humidity: {result['humid'].mean_humidity}% on {result['humid'].
          date.strftime('%B %d')}")             # Humid day of year


def print_monthly_report(result):
    if not result:
        print("No data for this month")
        return

    print(f"Highest Average: {result['avg_high']}C")          # Average of Highest Temp
    print(f"Lowest Average: {result['avg_low']}C")            # Average of Lowest Temp
    print(f"Average Mean Humidity: {result['avg_humid']}%")   # Average of Mean Humidity


def monthly_chart(readings, year, month):
    # Bar Charts for month (red -> high temp, blue -> low temp)
    month_data = sorted([i for i in readings if i.date.year == year and
                         i.date.month == month], key=lambda i: i.date)

    if not month_data:
        print("No data for this month")
        return

    month_name = month_data[0].date.strftime("%B %Y")
    print(f"{month_name}")

    for i in month_data:
        if i.max_temp is None or i.min_temp is None:
            continue
        day = f"{i.date.day:02d}"
        print(f"{day} {RED}{"+" * i.max_temp}{RESET} {PURPLE}{i.max_temp}C {RESET}")
        print(f"{day} {BLUE}{"+" * i.min_temp} {PURPLE}{i.min_temp}C {RESET}")


def horizontal_monthly_chart(readings, year, month):
    # Horizontal Bar Chart for month (red -> high temp, blue -> low temp)
    month_data = sorted([i for i in readings if i.date.year == year and
                         i.date.month == month], key=lambda i: i.date)

    if not month_data:
        print("No data for this month")
        return

    month_name = month_data[0].date.strftime("%B %Y")
    print(f"{month_name}")

    for i in month_data:
        if i.max_temp is None or i.min_temp is None:
            continue
        day = f"{i.date.day:02d}"

        print(f"{day} {BLUE}{"+" * i.min_temp}+{RED}{"+" * i.max_temp}"
              f"{PURPLE} {i.min_temp}C - {i.max_temp}C {RESET}")