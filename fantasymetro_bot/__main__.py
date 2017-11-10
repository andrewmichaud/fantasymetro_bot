"""Main class for fantasymetro_bot."""
import os
import random
import time
from datetime import datetime
from os import path
from shutil import copyfile

import botskeleton

import metro

HERE = path.abspath(path.dirname(__file__))
DELAY = 3600
METRO_CITY_OPTIONS = {
    "bayarea": {
        "long_name": "the Bay Area",
        "conf_file": "bayarea.yaml",
        "source_file": "bayarea.png",
    }
}

if __name__ == "__main__":
    SECRETS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "SECRETS")
    BOT_SKELETON = botskeleton.BotSkeleton(secrets_dir=SECRETS_DIR, bot_name="fantasymetro_bot",
                                           delay=DELAY)

    LOG = botskeleton.set_up_logging()

    metro_option = random.choice(list(METRO_CITY_OPTIONS.items()))

    while True:
        LOG.info("Generating a metro.")

        config_file = metro_option[1]["conf_file"]
        source_file = metro_option[1]["source_file"]
        source_file = os.path.join(HERE, source_file)
        long_name = metro_option[1]["long_name"]
        short_name = metro_option[0]

        out_file = "out.png"
        now = datetime.now()
        out_file_copy = f"{short_name} {datetime.strftime(now, '%Y-%M-%d %H:%M')}.png"

        # Produce out file.
        metro.gen(config_file, source_file, out_file)

        # Back up out file.
        copyfile(out_file, out_file_copy)

        LOG.info("Sending fantasy metro tweet.")

        BOT_SKELETON.send_with_one_media(f"Fantasy metro for {long_name}", out_file)

        BOT_SKELETON.nap()
