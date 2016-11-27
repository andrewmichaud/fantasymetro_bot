"""StationSet object, Station object, and methods for producing them from YAMl config files."""
import logging

import yaml

LOG = logging.getLogger("root")


class StationSet(object):
    def __init__(self):
        self.name = None
        self.real_stations = set()
        self.fantasy_stations = set()

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

    # TODO do something about that None.
    station.x = yaml.get("long", None)
    station.y = yaml.get("lat", None)

    return station


def stationset_from_yaml(yaml):
    """Produce StationSet from YAML."""
    station_set = StationSet()

    LOG.debug("Loading name for stationset from config YAML.")
    station_set.name = yaml.get("name", None)

    LOG.info("Loaded stationset %s from config.", station_set.name)

    # Get scale factors for later.
    long_shift = yaml.get("long_shift", 0)
    long_scale = yaml.get("long_scale", 1.0)

    lat_shift = yaml.get("lat_shift", 0)
    lat_scale = yaml.get("lat_scale", 1.0)

    print(long_shift)

    station_set.real_stations = set()
    station_set.fantasy_stations = set()

    LOG.debug("Loading real stations from config YAML.")
    real_stations_yaml = yaml.get("real_stations", [])
    for station_yaml in real_stations_yaml:
        station_set.real_stations.add(station_from_yaml(station_yaml))

    LOG.debug("Transforming real station coords according to scale factors.")
    for s in station_set.real_stations:
        s.x = (s.x * long_scale) + long_shift
        s.y = (s.y * lat_scale) + lat_shift
        print(s.x, s.y)

    LOG.debug("Loaded real stations %s.", station_set.real_stations)

    LOG.debug("Loading fantasy stations from config YAML.")
    fantasy_stations_yaml = yaml.get("fantasy_stations", [])
    for station_yaml in fantasy_stations_yaml:
        station_set.fantasy_stations.add(station_from_yaml(station_yaml))

    LOG.debug("Transforming fantasy station coords according to scale factors.")
    for s in station_set.fantasy_stations:
        s.x = (s.x * long_scale) + long_shift
        s.y = (s.y * lat_scale) + lat_shift

    LOG.debug("Loaded fantasy stations %s.", station_set.fantasy_stations)

    return station_set


def load(filename):
    """Load StationSet from a YAML file."""

    with open(filename, "r") as stream:
        LOG.debug("Opening stationset config file to retrieve stationset.")
        yaml_stationset = yaml.safe_load(stream)

    pretty_stationset = yaml.dump(yaml_stationset, width=1, indent=4)
    LOG.debug("Retrieved YAML from stationset file: %s", pretty_stationset)

    return stationset_from_yaml(yaml_stationset)
