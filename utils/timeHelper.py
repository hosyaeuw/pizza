from datetime import date


class DateHelper:
    @staticmethod
    def add_years(d, years):
        try:
            # Return same day of the current year
            return d.replace(year=d.year + years)
        except ValueError:
            return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))