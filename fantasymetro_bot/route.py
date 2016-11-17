"""Module for Routes."""
import copy
import logging
import math
import random

LOG = logging.getLogger("root")

ROUTE_STATIONS_RANGE = range(4, 10)

# yep, this is all of them
COLORS = ["purple", "blue", "green", "yellow", "orange", "red", "pink", "teal"]


class Route(object):
    """Object representing a Route through several Stations."""
    def __init__(self, station_set, chosen_colors=None):

        # Pick an un-chosen color at random.
        if chosen_colors is not None:
            LOG.debug("Choosing random color from provided list of unchosen colors.")
            self.color = random.choice([color for color in COLORS if color not in chosen_colors])
            # TODO handle if options == []

        else:
            LOG.debug("Choosing random color from global colors list.")
            self.color = random.choice(COLORS)

        # Generate route.
        remaining = copy.copy(station_set.stations)
        terminus = random.choice(list(remaining))
        remaining.discard(terminus)
        self.stations = [terminus]
        self.start = terminus
        LOG.debug("Chose %s as start terminus.", self.start)

        # For now, let's say route takes first terminus' name. May change later.
        self.name = terminus.name
        LOG.debug("Chose %s as route name.", self.name)

        num_stations = random.choice(ROUTE_STATIONS_RANGE)
        if num_stations > len(remaining):
            LOG.debug("Capping num_stations to %s (was %s).", len(remaining), num_stations)
            num_stations = len(remaining)

        LOG.debug("Creating route with %s stations.", num_stations)

        last = self.stations[-1]
        last_slope = None
        for i in range(num_stations-1):

            # Naive random:
            # Problems: routes zig-zag too much.
            # station = random.choice(list(remaining))

            # Random preferring closer stations.
            # Problem: sometimes real metros have long distances between stations, and this doesn't
            # capture that.
            # (will *never* generate BART bay tunnel)
            # x, y = (last.x, last.y)
            # ds = {math.sqrt((x - o.x)**2 + (y - o.y)**2): o for o in remaining}
            #
            # sorted_distance_ranking = sorted(ds.items())
            #
            # station = random.choice(sorted_distance_ranking[:3])[1]

            # Try to prefer straight lines?
            # Naive slope.
            # not quite - doesn't actually prefer straight lines like I was hoping.
            if last_slope is None:
                station = random.choice(list(remaining))

            else:
                slopes = {abs((last.y - o.y/last.x - o.x) - last_slope): o for o in remaining}

                sorted_slopes_ranking = sorted(slopes.items())

                station = random.choice(sorted_slopes_ranking[:4])[1]

            last_slope = last.y - station.y / last.x - station.x

            remaining.discard(station)
            self.stations.append(station)

        self.end = self.stations[-1]
        self.stations = self.stations[:-1]

    def __repr__(self):
        first_line = "Route(name: '{}', color: '{}')\n".format(self.name, self.color)

        second_line = "[{}]".format(self.start.name)

        for station in self.stations[1:-1]:
            second_line += "--({})".format(station.name)

        second_line += "--[{}]".format(self.end.name)

        return first_line + second_line
