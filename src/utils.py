from datetime import timedelta


def to_readable_time(minutes):
    delta = timedelta(minutes=minutes)
    return str(delta).split('.')[0]
