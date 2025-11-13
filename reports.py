from weather_report_console_view import WeatherReportConsoleView


class WeatherReport:
    def __init__(self):
        self.weather_report_view = WeatherReportConsoleView()

    def print_yearly_report(self, result):
        self.weather_report_view.print_yearly_report(result)

    def print_monthly_report(self, result, year=None, month=None):
        self.weather_report_view.print_monthly_report(result, year, month)

    def display_chart(self, readings, year, month, horizontal=False):
        self.weather_report_view.display_chart(readings, year, month, horizontal)
