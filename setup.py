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

      install_requires=["Pillow", "pyyaml>=3.12", "botskeleton>=1.1.0"],

      license="BSD3",

      name="fantasy_metro_bot",

      packages=find_packages(),

      python_requires=">=3.6",

      url="https://github.com/andrewmichaud/fantasymetro_bot",

      version=VERSION)
