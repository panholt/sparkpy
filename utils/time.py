from datetime import datetime


def ts_to_dt(ts):
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')

def dt_to_ts(dt=None):
    if not dt:
        dt = datetime.now()
    assert isinstance(dt, datetime)
    return dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
