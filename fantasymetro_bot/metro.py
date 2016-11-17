"""Module for a Metro, a set of Routes."""
import random

import route
import stationset


class Metro(object):
    """A Metro is a set of Routes."""
    def __init__(self, name, routes):
        self.name = name
        self.routes = routes

    def __repr__(self):
        out = "Metro(name: {})\n".format(self.name)
        for i, r in enumerate(self.routes):
            out += repr(r)
            if i < len(self.routes)-1:
                out += "\n"

        return out


if __name__ == "__main__":
    station_set = stationset.load("sfmetro.yaml")

    NUM_ROUTES_RANGE = range(3, 7)

    num_routes = random.choice(NUM_ROUTES_RANGE)

    routes = []
    for i in range(num_routes):
        routes.append(route.Route(station_set))

    metro = Metro(routes=routes, name=station_set.name)
    print(repr(metro))
