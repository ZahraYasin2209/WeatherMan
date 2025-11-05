def yearly_calculations(readings, year):
    # Returns highest, lowest and most humid day in a year
    year_data = [i for i in readings if i.date.year == year]
    if not year_data:
        return 0

    highest_temp = max((i for i in year_data if i.max_temp is not None),
                key=lambda i: i.max_temp)
    lowest_temp = min((i for i in year_data if i.min_temp is not None),
                key=lambda i: i.min_temp)
    mean_humid = max((i for i in year_data if i.mean_humidity is not None),
                key=lambda i: i.mean_humidity)

    return {
        "highest": highest_temp,
        "lowest": lowest_temp,
        "humid": mean_humid,
    }


def monthly_average(readings, year, month):
    # Return the average of highest, lowest and mean humidity
    month_data = [i for i in readings if i.date.year == year and i.date.month == month]
    if not month_data:
        return 0

    avg_highest = round(sum(i.max_temp for i in month_data if i.max_temp is not None) /
                     len([i for i in month_data if i.max_temp is not None]))

    avg_lowest = round(sum(i.min_temp for i in month_data if i.min_temp is not None) /
                 len([i for i in month_data if i.min_temp is not None]))

    avg_humidity = round(sum(i.mean_humidity for i in month_data if i.mean_humidity is not None) /
                 len([i for i in month_data if i.mean_humidity is not None]))

    return {
        "avg_high": avg_highest,
        "avg_low": avg_lowest,
        "avg_humid": avg_humidity,
    }

