import time


class STRING(object):
    pass


class BINARY(object):
    """binary encoded string"""
    pass


class NUMBER(object):
    """numberic data types"""
    pass


class DATETIME(object):
    """datetime objects"""
    pass


class ROWID(object):
    pass


def Binary(string):
    pass


def Date(year, month, day):
    pass


def Time(hour, minute, second):
    pass


def Timestamp(year, month, day, hour, minute, second):
    pass


def DateFromTicks(ticks):
    return Date(*time.localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return Time(*time.localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return Timestamp(*time.localtime(ticks)[:6])
