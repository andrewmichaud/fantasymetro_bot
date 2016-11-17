from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, "VERSION"), encoding="utf-8") as f:
    VERSION = f.read().strip()

setup(author="Andrew Michaud",
      author_email="bots+fantasymetro@mail.andrewmichaud.com",

      entry_points={
          "console_scripts": ["fantasy_metro_bot = fantasy_metro_bot.__main__:main"]
      },

      install_requires=["pillow>=3.4.2", "pyyaml>=3.12""tweepy>=3.5"],

      license="BSD3",

      name="fantasy_metro_bot",

      packages=find_packages(),

      # Project"s main homepage
      url="https://github.com/andrewmichaud/fantasymetro_bot",

      version=VERSION)
