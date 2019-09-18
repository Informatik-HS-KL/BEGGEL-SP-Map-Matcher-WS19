"""

"""

class Node:

    def __init__(self, id: int, latlon: tuple):
        self.__id = id
        self.__latLon = latlon
        self.__tags = {}
        self.__links = []

    def getLinks(self):
        """"""
        return self.__links

    def getId(self):
        return self.__id

    def getLatLon(self):
        return self.__latLon

    def setTags(self, tags: dict):
        self.__tags = tags

    def addLink(self, link):
        self.__links.append(link)

    def __repr__(self):
        return "<Node: %s>" % (self.__id)