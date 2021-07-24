from datetime import datetime

months = ["Jan", "Feb", "Mar", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]


def full(unix):
    ts = int(unix)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def half(unix):
    ts = int(unix)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')


def am(unix):
    ts = int(unix)
    month = months[datetime.utcfromtimestamp(ts).month - 1]
    year = datetime.utcfromtimestamp(ts).year
    day = datetime.utcfromtimestamp(ts).day
    return "%s %i, %i" % (month, day, year)


