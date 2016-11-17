"""Module for Routes."""
import copy
import random


ROUTE_STATIONS_RANGE = range(4, 10)

# yep, this is all of them
COLORS = ["purple", "blue", "green", "yellow", "orange", "red", "pink", "teal"]


class Route(object):
    """Object representing a Route through several Stations."""
    def __init__(self, station_set, chosen_colors=None):

        # Pick an un-chosen color at random.
        if chosen_colors is not None:
            random.choice([color for color in COLORS if color not in chosen_colors])
            # TODO handle if options == []

        else:
            self.color = random.choice(COLORS)

        # Generate route.
        remaining = copy.copy(station_set.stations)
        terminus = random.choice(list(remaining))
        remaining.discard(terminus)
        self.stations = [terminus]
        self.start = terminus

        # For now, let's say route takes first terminus' name. May change later.
        self.name = terminus.name

        num_stations = random.choice(ROUTE_STATIONS_RANGE)
        if num_stations > len(remaining):
            num_stations = len(remaining)

        for i in range(num_stations-1):
            station = random.choice(list(remaining))
            remaining.discard(station)
            self.stations.append(station)

        self.end = self.stations[-1]

    def __repr__(self):
        first_line = "Route(name: '{}', color: '{}')\n".format(self.name, self.color)

        second_line = "[{}]".format(self.start.name)

        for station in self.stations[1:-1]:
            second_line += "--({})".format(station.name)

        second_line += "--[{}]".format(self.end.name)

        return first_line + second_line
