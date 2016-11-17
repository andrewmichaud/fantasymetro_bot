"""Module for a Metro, a set of Routes."""
import os
import sys
import random
from shutil import copyfile

from PIL import Image, ImageDraw

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

    def draw(self, filename):
        """Draw metro onto image."""

        base, ext = os.path.splitext(filename)
        draw_copy = base + "-drawn" + ext
        copyfile(filename, draw_copy)

        im = Image.open(draw_copy)

        width, height = im.size
        print("Image is wxh {}x{}".format(width, height))

        draw = ImageDraw.Draw(im)

        for r in self.routes:
            # Draw start.
            RADIUS = 5
            draw.ellipse([r.start.x - RADIUS, r.start.y - RADIUS,
                          r.start.x + RADIUS, r.start.y + RADIUS],
                         outline=r.color)
            draw.text((r.start.x, r.start.y), r.start.name, fill="black")
            last = (r.start.x, r.start.y)

            for s in r.stations[1:-1]:
                draw.line([last, (s.x, s.y)], fill=r.color, width=3)
                draw.ellipse([s.x - RADIUS, s.y - RADIUS,
                              s.x + RADIUS, s.y + RADIUS],
                             outline=r.color, fill=r.color)

                draw.text((s.x, s.y), s.name, fill="black")

                last = (s.x, s.y)

            draw.line([last, (r.end.x, r.end.y)], fill=r.color, width=3)
            draw.ellipse([r.end.x - RADIUS, r.end.y - RADIUS,
                          r.end.x + RADIUS, r.end.y + RADIUS],
                         outline=r.color)

            draw.text((r.end.x, r.end.y), r.end.name, fill="black")

            # draw.line((0, 0) + im.size, fill="red", width=3)

        # write to stdout
        im.save(draw_copy)


if __name__ == "__main__":
    station_set = stationset.load("bayarea.yaml")

    NUM_ROUTES_RANGE = range(3, 7)

    num_routes = random.choice(NUM_ROUTES_RANGE)

    routes = []
    for i in range(num_routes):
        routes.append(route.Route(station_set))

    metro = Metro(routes=routes, name=station_set.name)
    print(repr(metro))

    metro.draw("bayarea.png")
