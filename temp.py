import datetime
import calendar


def get_day_name(month: int, year: int) -> list[str]:
    days = [
        calendar.day_abbr[x]
        for x in [
            calendar.weekday(year, month, x)
            for x in [
                y for x in calendar.monthcalendar(year, month) for y in x if y != 0
            ]
        ]
    ]
    return [day.upper() if day == "Sat" or day == "Sun" else day for day in days]


def get_day_month(month: int, year: int) -> list[str]:
    return [
        f"{str(date)}-{calendar.month_abbr[month]}"
        for date in [
            y for x in calendar.monthcalendar(year, month) for y in x if y != 0
        ]
    ]


# print(get_day_name(datetime.datetime.today().month, datetime.datetime.today().year))
print(get_day_month(datetime.datetime.today().month, datetime.datetime.today().year))
