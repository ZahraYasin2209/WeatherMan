""" Returns highest, lowest temperature and most humid day in a year """
def yearly_calculations(readings, year):
    year_data = [reading for reading in readings if reading.date.year == year]

    valid_readings = {
        "max_temp": [reading for reading in year_data if reading.max_temp is not None],
        "min_temp": [reading for reading in year_data if reading.min_temp is not None],
        "mean_humidity": [reading for reading in year_data if reading.mean_humidity is not None],
     }

    highest_temp = max(valid_readings["max_temp"],
                       key=lambda reading: reading.max_temp, default=None)
    lowest_temp = max(valid_readings["min_temp"],
                      key=lambda reading: reading.min_temp, default=None)
    mean_humidity = max(valid_readings["mean_humidity"],
                        key=lambda reading: reading.mean_humidity, default=None)

    return {
        "highest": highest_temp,
        "lowest": lowest_temp,
        "humid": mean_humidity,
    }


""" Helper function to calculate average """
def calculate_average(values):
    valid_values = [valid for valid in values if valid is not None]
    if valid_values:
        return round(sum(valid_values) / len(valid_values))
    else:
        return None


""" Returns average of highest, lowest temperature and mean humidity """
def monthly_average(readings, year, month):
    monthly_records = [reading for reading in readings if reading.date.year == year
                       and reading.date.month == month]

    avg_highest = calculate_average(reading.max_temp for reading in monthly_records)
    avg_lowest = calculate_average(reading.min_temp for reading in monthly_records)
    avg_humidity = calculate_average(reading.mean_humidity for reading in monthly_records)

    return {
        "highest_average_temp": avg_highest,
        "lowest_average_temp": avg_lowest,
        "average_mean_humidity": avg_humidity,
    }
