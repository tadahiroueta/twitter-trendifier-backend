import datetime


def deformDate(date: str) -> datetime.datetime:
    """
    Returns the an object of datetime.
    
    Arguments:
        date: date in YYYY-MM-DD format
    """
    return datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:10]))


def formatDate(date: datetime.datetime) -> str:
    """
    Returns the date in YYYY-MM-DD format.
    
    Arguments:
        date: date as a datetime object
    """
    return date.strftime("%Y-%m-%d")


def getToday():
    """Returns today's date as a datetime object."""
    return datetime.datetime.now()


def getRelativeDate(days: int, date=getToday()) -> datetime.datetime:
    """
    Returns the date n days from today (or the specified date).
    
    Arguments:
        days: number of days from today (accepts negative values)
    """
    return date + datetime.timedelta(days=days)


def getNextDay(date: datetime.datetime) -> datetime.datetime:
    """
    Arguments:
        date: date as a datetime object
    """
    return getRelativeDate(1, date=date)


def formatShortDate(date: datetime.datetime) -> str:
    """
    Formats a date in the format MM/DD.

    Arguments:
        date: date as a datetime object
    """
    return date.strftime('%m/%d')


def getContinuosDates() -> list:
    """Returns a list of 31 dates (inclusive) in the format MM/DD leading up to today."""
    return [formatShortDate(getRelativeDate(days)) for days in range(-30, 1)]
    
    
def getWeeklyDates() -> list:
    """Returns a list of 31 dates (inclusive) in the format MM/DD leading up to today, with weekly intervals."""
    return [formatShortDate(getRelativeDate(days)) for days in range(-210, 1, 7)]
