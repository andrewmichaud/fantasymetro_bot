"""StationSet object, Station object, and methods for producing them from YAMl config files."""
import logging

import yaml

LOG = logging.getLogger("root")


class StationSet(object):
    def __init__(self):
        self.name = None
        self.stations = set()

    def __repr__(self):
        return "StationSet(name: '{}', stations: {})".format(self.name, self.stations)


class Station(object):
    """Object representing a metro station."""
    def __init__(self):
        self.name = None
        self.x = None
        self.y = None

    def __repr__(self):
        return "Station(name: '{}', x: {}, y: {})".format(self.name, self.x, self.y)


def station_from_yaml(yaml):
    """Produce Station from YAML."""
    station = Station()

    station.name = yaml.get("name", None)
    station.x = yaml.get("x", None)
    station.y = yaml.get("y", None)

    return station


def stationset_from_yaml(yaml):
    """Produce StationSet from YAML."""
    station_set = StationSet()

    station_set.name = yaml.get("name", None)
    station_set.stations = set()
    stations_yaml = yaml.get("stations", [])
    for station_yaml in stations_yaml:
        station_set.stations.add(station_from_yaml(station_yaml))

    return station_set


def load(filename):
    """Load StationSet from a YAML file."""

    with open(filename, "r") as stream:
        LOG.debug("Opening stationset config file to retrieve stationset.")
        yaml_stationset = yaml.safe_load(stream)

    pretty_stationset = yaml.dump(yaml_stationset, width=1, indent=4)
    LOG.debug("Retrieved YAML from stationset file: %s", pretty_stationset)

    return stationset_from_yaml(yaml_stationset)
