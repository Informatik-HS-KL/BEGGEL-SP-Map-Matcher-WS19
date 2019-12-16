"""
Description: Creates special Config Class for parsing and getting configurations
see __init__.py für instanceiating during runtime
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

import os
from configparser import ConfigParser, NoSectionError


class MapServiceConfig(ConfigParser):

    def __call__(self):
        super()
        print("Config Class call")

    def options(self, section, no_defaults=False, **kwargs):
        """
        Options gibt alle einträge einer Section zurück.
        überschriebene Methode, die dafür sorgt, dass in Options die DEFAULT Section nicht geladen wird
        """
        if no_defaults:
            try:
                return list(self._sections[section].keys())
            except KeyError:
                raise NoSectionError(section)
        else:
            return super().options(section, **kwargs)


def get_config():
    """
    :return: MapServiceConfig-Objects
    """
    conf = MapServiceConfig()
    conf.read(os.path.dirname(__file__) + "/config.ini")

    return conf


CONFIG = get_config()
print("config.py loaded")