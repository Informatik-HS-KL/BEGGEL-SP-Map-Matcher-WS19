"""
Läd daten von der OVerpass schnittstelle in eine Kachel
"""

class OverPassWrapper:

    def loadTile (self, geoHash):
        """ Daten von der Overpass api laden
            from geohash to Boundingbox
        """

        # url = "%s?data=[out:json];area[name=Kaiserslautern];way[name='Dansenberger Straße'];>;<;out;" % (self.root_url)
        # print(url)
        # resp = requests.get(url)
        # data = resp.json()

        # nodes = {}
        # for way in ways:
        #     for node in way.nodes:
        #         nodes.update({node: []})


        return tile