from datetime import datetime


def ts_to_dt(ts):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
