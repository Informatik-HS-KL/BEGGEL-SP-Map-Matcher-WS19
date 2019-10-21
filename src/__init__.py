from src.config import MapServiceConfig
import sys, os

def get_config():

    CONFIG = MapServiceConfig()
    CONFIG.read(os.path.dirname(__file__) + "/config.ini")

    return CONFIG

CONFIG = get_config()