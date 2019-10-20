from configparser import ConfigParser, NoSectionError


class MapServiceConfig(ConfigParser):

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


print("config.py loaded")