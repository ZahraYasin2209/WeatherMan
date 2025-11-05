import os
import csv
from datetime import datetime
from class_model import WeatherReadings


def parse_weather_files(directory):
    # Parse all weather files present in directory
    readings = []           # returns list of WeatherReadings object

    for filename in os.listdir(directory):
        file_path = os.path.join(directory,
                                 filename)

        if os.path.isdir(file_path):            # skip directories
            continue
        if not filename.endswith(".txt"):
            continue

        with open(file_path, 'r') as file:      # reading .txt files
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    date = datetime.strptime(row["PKT"],"%Y-%m-%d").date()
                    max_temp = int(row["Max TemperatureC"] if row["Max TemperatureC"]
                                   else "None")
                    min_temp = int(row["Min TemperatureC"] if row["Min TemperatureC"]
                                   else "None")
                    mean_humidity = int(row[" Mean Humidity"] if row[" Mean Humidity"]
                                        else "None")

                    readings.append(WeatherReadings(date, max_temp, min_temp, mean_humidity))
                except (ValueError, KeyError):
                    continue
    return readings