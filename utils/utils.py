import datetime
from dateutil.relativedelta import relativedelta

def format_datetime(dt):
    if not dt:
        return ''
    return datetime.datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")


def str_to_datetime4(s):
    if not s:
        return None
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def now_to_datetime4():
    return str_to_datetime4(format_datetime(datetime.datetime.now()))


def five_minutes_later(dt):
    return str_to_datetime4(format_datetime(dt)) + relativedelta(minutes=5)
