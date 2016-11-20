"""Module for Routes."""
import copy
import logging
import math
import random

LOG = logging.getLogger("root")

STATIONS_RANGE = range(5, 8)

# yep, this is all of them
COLORS = ["purple", "blue", "green", "yellow", "orange", "red", "magenta", "teal"]


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

        self.station_gen(station_set)

        # For now, let's say route takes first terminus' name. May change later.
        self.name = self.start.name
        LOG.debug("Chose %s as route name.", self.name)

    def station_gen(self, station_set):  # alg=NEARNESS_SLOPE_COMBINED_RANKING):
        """Generate list of stations for this route from a list of possible stations."""
        # TODO use param that comes in

        # Generate route.
        remaining_real = copy.copy(station_set.real_stations)
        remaining_fantasy = copy.copy(station_set.fantasy_stations)

        self.start = random.choice(list(remaining_real))
        remaining_real.discard(self.start)

        self.stations = []
        LOG.debug("Chose %s as start terminus.", self.start)

        num_stations = random.choice(STATIONS_RANGE)
        if num_stations > len(remaining_real):
            LOG.debug("Capping num_stations to %s (was %s).", len(remaining_real), num_stations)
            num_stations = len(remaining_real)

        LOG.debug("Picking %s stations for this route.", num_stations)

        # Decide on stations for route.
        one_ago = None
        two_ago = None
        for i in range(num_stations-1):
            # Choose next stations that will give you large angles compared to the last station.
            # Pick first two stations randomly.
            # Calculate length of line segment between one_ago station and two_ago station.

            if one_ago is None and two_ago is None:
                two_ago = random.choice(list(remaining_real))
                remaining_real.discard(two_ago)

                one_ago = random.choice(list(remaining_real))
                remaining_real.discard(one_ago)

            # Add fantasy stations at random.
            perc = random.uniform(0, 1)
            if perc < 0.30:
                stations_list = list(remaining_fantasy)
                real = False

            else:
                stations_list = list(remaining_real)
                real = True

            angs = {station_calc_ang(station, one_ago, two_ago): station for station in
                    stations_list}
            sorted_station_ranking = sorted(angs.items(), reverse=True)
            LOG.debug("Sorted stations: {}".format(sorted_station_ranking))

            perc = random.uniform(0, 1)
            if perc > 0.20:
                LOG.debug("Trying to force path angle >= 140 degrees")
                options = [(val, station) for val, station in sorted_station_ranking if val >= 140]

                if len(options) < 2:
                    options = sorted_station_ranking[:2]

            elif perc <= 0.20 and perc > 0.0:
                LOG.debug("Trying to force path angle >= 100 degrees")
                options = [(val, station) for val, station in sorted_station_ranking if val >= 110]

                if len(options) < 2:
                    options = sorted_station_ranking[:2]

            else:
                LOG.debug("Picking whatever kind of angle.")
                options = sorted_station_ranking

            station = random.choice(options)[1]
            if real:
                remaining_real.discard(station)
            else:
                remaining_fantasy.discard(station)

            self.stations.append(station)

            two_ago = one_ago
            one_ago = station

        self.end = self.stations[-1]
        self.stations = self.stations[:-1]

        self.all_stations = [self.start] + self.stations + [self.end]

    def __repr__(self):
        first_line = "Route(name: '{}', color: '{}')\n".format(self.name, self.color)

        second_line = "[{}]".format(self.start.name)

        for station in self.stations[1:-1]:
            second_line += "--({})".format(station.name)

        second_line += "--[{}]".format(self.end.name)

        return first_line + second_line


def station_dist(s1, s2):
    """Calculate distance between two stations. Wrapper around standard dist."""
    return dist((s1.x, s1.y), (s2.x, s2.y))


def dist(p1, p2):
    """Calculate distance between two points with standard distance formula."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def calc_ang(a, b, c):
    """
    Calculate angle lambda given the lengths of three sides of a triangle.
    a and be are the sides surrounding the angle we want to know about.
    c is the angle across from it.
    """
    try:
        return math.acos(
            (a**2 + b**2 - c**2) /
            (2*a*b)
        ) * 180 / math.pi
        # fucking radians

    except ValueError as e:
        # TODO figure out what the domain error is here. I suspect we're getting angles >180, but I
        # haven't actually dug into it.
        LOG.error("Received math.ValueError %s", e)
        LOG.error("Ignoring it and returning 180 degrees as angle.")
        return 180


def station_calc_ang(station, one_ago, two_ago):
    """
    Calculate angle if we add new station to the route currently including one_ago and two_ago.
    """

    a = station_dist(two_ago, one_ago)

    # wow this diagram is garbage
    # 2-ago station, 1-ago station, station we'd like to add.
    # 2A
    # * *
    # *   *
    # *     *
    # a       *
    # *         *
    # *           c
    # 1A            *
    #     *           *
    #         *         *
    #             b       *
    #                 *     *
    #                     *   *
    #                         NP

    b = station_dist(one_ago, station)
    c = station_dist(station, two_ago)

    return calc_ang(a, b, c)

# abandoned algs for generating routes.
# ALG_NAIVE_RANDOM
# Naive random:
# Problems: routes zig-zag too much.
# station = random.choice(list(remaining))

# ALG_DISTANCE
# Random preferring closer stations.
# Pick between top N=3 closet stations.
# Problem: sometimes real metros have long distances between stations, and this doesn't
# capture that.
# (will *never* generate BART bay tunnel)
# x, y = (last.x, last.y)
# ds = {math.sqrt((x - o.x)**2 + (y - o.y)**2): o for o in remaining}
#
# sorted_distance_ranking = sorted(ds.items())
#
# station = random.choice(sorted_distance_ranking[:3])[1]

# ALG_DISTANCE_BUCKETED
# Random preferring closer stations, but allowing farther stations sometimes.
# naaaah
# x, y = (last.x, last.y)
# ds = {math.sqrt((x - o.x)**2 + (y - o.y)**2): o for o in remaining}
#
# sorted_distance_ranking = sorted(ds.items())
#
# perc = random.uniform(0, 1)
#
# if perc > 0.6:
#     station = random.choice(sorted_distance_ranking[:2])[1]
#
# elif perc > 0.1 and perc <= 0.6:
#     station = random.choice(sorted_distance_ranking[:5])[1]
#
# else:
#     station = random.choice(sorted_distance_ranking[:-4])[1]

# ALG_SLOPE
# Try to prefer straight lines?
# Naive slope.
# Pick between top 4 stations with closet slope to previous slope.
# Not quite - still lots of zig zags.
# Does get short-distance runs, which is nice.
# if last_slope is None:
#     station = random.choice(list(remaining))
#
# else:
#     slopes = {abs((last.y - o.y/last.x - o.x) - last_slope): o for o in remaining}
#
#     sorted_slopes_ranking = sorted(slopes.items())
#
#     station = random.choice(sorted_slopes_ranking[:4])[1]
#
# last_slope = last.y - station.y / last.x - station.x
