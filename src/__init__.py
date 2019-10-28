"""
Description: Creates incstance of own configparser as Global Variable for Runtime
see __init__.py für instanceiating during runtime
@date: 10/25/2019
@author: Lukas Felzmann, Sebastian Leilich, Kai Plautz
"""

from src.config import MapServiceConfig
import sys, os

def get_config():

    CONFIG = MapServiceConfig()
    CONFIG.read(os.path.dirname(__file__) + "/config.ini")

    return CONFIG

CONFIG = get_config()