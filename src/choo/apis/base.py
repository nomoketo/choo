import json
import os

import defusedxml.ElementTree as ET
from defusedxml import minidom


class API:
    LocationQuery = None
    AddressQuery = None
    StopQuery = None
    POIQuery = None
    TripQuery = None

    def __init__(self, name):
        if self.__class__ == API:
            raise TypeError('Only API subclasses can be initialized.')
        self.name = name

    @property
    def locations(self):
        if self.StopQuery is None:
            raise NotImplementedError('Querying locations is not supported by this network.')
        return self.LocationQuery(self)

    @property
    def addresses(self):
        if self.AddressQuery is None:
            raise NotImplementedError('Querying addresses is not supported by this network.')
        return self.AddressQuery(self)

    @property
    def stops(self):
        if self.StopQuery is None:
            raise NotImplementedError('Querying stops is not supported by this network.')
        return self.StopQuery(self)

    @property
    def pois(self):
        if self.POIQuery is None:
            raise NotImplementedError('Querying POIs is not supported by this network.')
        return self.POIQuery(self)

    @property
    def trips(self):
        if self.TripQuery is None:
            raise NotImplementedError('Querying trips is not supported by this network.')
        return self.TripQuery(self)


class ParserError(Exception):
    def __init__(self, parser, message):
        self.parser = parser
        self.message = message
        self.pretty_data = self.parser.printable_data()

        if os.environ.get('CHOO_DEBUG'):
            message += '\n'+self.pretty_data

        super().__init__(message)
        self.message = self.actual


class Parser:
    def __init__(self, parent, data, *args, **kwargs):
        self.network = parent.network
        self.time = parent.time
        self.data = data
        self._args = args
        self._kwargs = kwargs

    def printable_data(self, pretty=True):
        raise NotImplementedError


class XMLParser(Parser):
    def printable_data(self, pretty=True):
        string = ET.tostring(self.data, 'utf-8')
        if pretty:
            string = minidom.parseString(string).toprettyxml(indent='  ')
        return string


class JSONParser(Parser):
    def printable_data(self, pretty=True):
        return json.dumps(self.data, indent=2 if pretty else None)


class parser_property(object):
    def __init__(self, func, name=None):
        self.func = func
        self.name = name or func.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        field = obj.Model._fields[self.name]
        value = obj.__dict__[self.name] = self.func(obj, obj.data, *obj._args, **obj._kwargs)

        if not field.validate(value):
            raise TypeError('Invalid type for attribute %s.' % self.name)

        return value

    def __set__(self, obj, value):
        raise AttributeError("can't set a parser property")

    def __delete__(self, obj):
        raise AttributeError("can't delete a parser property")


def cached_property(func):
    def wrapped_func(self):
        value = func(self, self.data, *self._args, **self._kwargs)
        self.__dict__[func.__name__] = value
        return value
    return property(wrapped_func)