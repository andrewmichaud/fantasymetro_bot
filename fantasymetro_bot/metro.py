"""Module for a Metro, a set of Routes."""
import os
import random
from shutil import copyfile

from PIL import Image, ImageDraw, ImageFont

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

        font = ImageFont.truetype("DejaVuSerif.ttf", 16)
        width, height = im.size
        print("Image is wxh {}x{}".format(width, height))

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
                draw.text((s.x+RADIUS, s.y+RADIUS), s.name, fill="red", font=font)

        # Save image.
        im.save(draw_copy)


if __name__ == "__main__":
    station_set = stationset.load("bayarea.yaml")

    NUM_ROUTES_RANGE = range(3, 5)

    num_routes = random.choice(NUM_ROUTES_RANGE)

    routes = []
    chosen_colors = []
    for i in range(num_routes):
        r = route.Route(station_set, chosen_colors=chosen_colors)
        chosen_colors.append(r.color)
        routes.append(r)

    metro = Metro(routes=routes, name=station_set.name)
    print(repr(metro))

    metro.draw("bayarea.png")
