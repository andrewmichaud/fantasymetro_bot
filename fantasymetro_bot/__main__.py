"""Main class for fantasymetro_bot."""
import random
import time
from datetime import datetime
from shutil import copyfile

import tweepy

import metro
import send
import util

DELAY = 3600
METRO_CITY_OPTIONS = {
    "bayarea": {
        "long_name": "the Bay Area",
        "conf_file": "bayarea.yaml",
        "source_file": "bayarea.png",
    }
}

if __name__ == "__main__":
    api = send.auth_and_get_api()

    LOG = util.set_up_logging()

    metro_option = random.choice(list(METRO_CITY_OPTIONS.items()))

    while True:
        LOG.info("Generating a metro.")

        config_file = metro_option[1]["conf_file"]
        source_file = metro_option[1]["source_file"]
        long_name = metro_option[1]["long_name"]
        short_name = metro_option[0]

        out_file = "out.png"
        now = datetime.now()
        out_file_copy = short_name + " " + datetime.strftime(now, "%Y-%M-%d %H:%M") + ".png"

        # Produce out file.
        metro.gen(config_file, source_file, out_file)

        # Back up out file.
        copyfile(out_file, out_file_copy)

        LOG.info("Sending fantasy metro tweet.")

        try:
            api.update_with_media(out_file, status="Fantasy metro for {}".format(long_name))

        except tweepy.TweepError as e:
            LOG.critical("A Tweepy error we don't know how to handle happened.")
            LOG.critical("Error reason: {}".format(e.reason))
            LOG.critical("Exiting.")
            break

        LOG.info("Sleeping for {} seconds.".format(DELAY))
        time.sleep(DELAY)
