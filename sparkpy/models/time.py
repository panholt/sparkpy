from datetime import datetime


class SparkTime(object):

    def __init__(self, *args):
        if args:
            self._ts = args[0]
            self._dt = datetime.strptime(self.ts, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            self._dt = datetime.now()
            self._ts = self.dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # Python datetime fun
            if len(self.ts) == 27:
                self._ts = self._ts[:23] + 'Z'
        return

    @property
    def ts(self):
        return self._ts

    @property
    def dt(self):
        return self._dt

    def __eq__(self, other):
        return self.dt == other

    def __ne__(self, other):
        return self.dt != other

    def __lt__(self, other):
        return self.dt < other

    def __le__(self, other):
        return self.dt <= other

    def __gt__(self, other):
        return self.dt > other

    def __ge__(self, other):
        return self.dt >= other

    def __hash__(self):
        return hash(self.ts)

    def __repr__(self):
        return self.ts
