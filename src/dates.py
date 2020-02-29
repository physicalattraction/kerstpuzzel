import json
from collections import defaultdict
from datetime import date, timedelta

sequence = [9, 11, 14, 15, 21, 23, 26, 29, 32, 37, 38, 40, 44, 45, 47, 50, 52, 53, 56, 59, 62, 63, 64, 67, 68, 69, 71,
            75, 76, 81, 82, 83, 86, 88, 92, 94, 97, 99, 101, 105, 111, 112, 116, 127, 128, 131, 134, 136, 140, 149, 153,
            157, 158, 160, 163, 164, 167, 171, 172, 173, 177, 179, 182, 183, 189, 191, 194, 197, 200, 211, 212, 223,
            225, 226, 227, 231, 232, 236, 239, 242, 251, 254, 255, 256, 257, 261, 263, 266, 268, 269, 273, 279, 280]


def days_of_week(year: int = 2019):
    first_day = 100


def dates(year: int = 2019) -> [date]:
    new_years_day = date(year=year, month=1, day=1)
    days = [new_years_day + timedelta(days=element - 1) for element in sequence]
    printable_days = [day.strftime('%a %d-%m') for day in days]
    printable_months = defaultdict(list)
    for day in days:
        printable_months[day.strftime('%b')].append(day.strftime('%a %d'))
    print(json.dumps(printable_months))
    return days


if __name__ == '__main__':
    dates()
