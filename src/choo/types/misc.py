from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import datetime, timedelta
from math import asin, cos, radians, sin, sqrt


class Serializable(ABC):
    @abstractmethod
    def serialize(self):
        pass

    @classmethod
    @abstractmethod
    def unserialize(cls, data):
        pass


class Coordinates(Serializable, namedtuple('Coordinates', ('lat', 'lon'))):
    """
    Coordinates in WGS84. Has a lat and lon attribute. Implemented as namedtuple.
    """
    def distance_to(self, other):
        """
        Get distance to other Coordinates object in meteres.
        """
        if not isinstance(other, Coordinates):
            raise TypeError('distance_to expected Coordinates object, not %s' % repr(other))

        lon1, lat1, lon2, lat2 = map(radians, [self.lon, self.lat, other.lon, other.lat])
        return 12742000 * asin(sqrt(sin((lat2-lat1)/2)**2+cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2))

    def serialize(self):
        return (self.lat, self.lon)

    @classmethod
    def unserialize(cls, data):
        return cls(*data)

    def __reversed__(self):
        return tuple(self)[::-1]


class LiveTime(Serializable, namedtuple('LiveTime', ('time', 'delay'))):
    def __new__(self, time, delay=None):
        if not isinstance(time, datetime):
            raise TypeError('time has to be datetime, not %s' % repr(time))

        if not isinstance(delay, timedelta):
            raise TypeError('delay has to be timedelta or None, not %s' % repr(delay))

        return super().__new__(time, delay)

    def __str__(self):
        out = self.time.strftime('%Y-%m-%d %H:%M')
        if self.delay is not None:
            out += ' %+d' % (self.delay.total_seconds() / 60)
        return out

    @property
    def is_live(self):
        return self.delay is not None

    @property
    def expected_time(self):
        if self.delay is not None:
            return self.time + self.delay
        else:
            return self.time