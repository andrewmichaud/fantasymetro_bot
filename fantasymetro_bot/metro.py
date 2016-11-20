"""Module for a Metro, a set of Routes."""
import logging
import os
import random
from shutil import copyfile

from PIL import Image, ImageDraw, ImageFont

import route
import stationset

LOG = logging.getLogger("root")


# Number of routes to put in the metro system.
NUM_ROUTES_RANGE = range(3, 6)


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

    def draw(self, source_image, dest_image):
        """Draw metro onto image."""

        base, ext = os.path.splitext(source_image)
        copyfile(source_image, dest_image)

        im = Image.open(dest_image)

        font = ImageFont.truetype("DejaVuSerif.ttf", 16)

        draw = ImageDraw.Draw(im)

        for r in self.routes:
            # Draw start.
            RADIUS = 6
            draw.ellipse([r.start.x - RADIUS, r.start.y - RADIUS,
                          r.start.x + RADIUS, r.start.y + RADIUS],
                         outline=r.color)
            last = (r.start.x, r.start.y)

            for s in r.stations:
                draw.line([last, (s.x, s.y)], fill=r.color, width=3)
                draw.ellipse([s.x - RADIUS, s.y - RADIUS,
                              s.x + RADIUS, s.y + RADIUS],
                             outline=r.color, fill=r.color)

                last = (s.x, s.y)

            draw.line([last, (r.end.x, r.end.y)], fill=r.color, width=3)
            draw.ellipse([r.end.x - RADIUS, r.end.y - RADIUS,
                          r.end.x + RADIUS, r.end.y + RADIUS],
                         outline=r.color)

        # Draw text last so it is at the top layer.
        for r in self.routes:
            for s in r.all_stations:
                draw.text((s.x+RADIUS, s.y+RADIUS), s.name, fill="purple", font=font)

        # Save image.
        im.save(dest_image)


def gen(config_file, source_image, dest_image):
    """Generate a fantasy metro system image."""
    station_set = stationset.load(config_file)
    LOG.debug("Producing fantasy metro system for %s.", station_set.name)

    num_routes = random.choice(NUM_ROUTES_RANGE)
    LOG.debug("Creating %s routes.", num_routes)

    routes = []
    chosen_colors = []
    for i in range(num_routes):
        r = route.Route(station_set, chosen_colors=chosen_colors)
        chosen_colors.append(r.color)
        routes.append(r)

    # Draw metro.
    metro = Metro(routes=routes, name=station_set.name)

    LOG.info("Drawing metro system for %s to %s", station_set.name, dest_image)
    metro.draw(source_image, dest_image)
