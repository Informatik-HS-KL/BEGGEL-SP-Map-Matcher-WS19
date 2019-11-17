from abc import ABC, abstractmethod

# Todo (14.11.2019, Lukas Felzmann): Eigentlich sind in LinkUser und den Unterklassen alle Methoden statisch. Zudem
#  macht es keinen Sinn, dass man zum Beispiel ein Objekt vom Typ Pedestrian erzeugen kann. Wir müssen uns an der
#  Stelle nochmal Gedanken über die Struktur/Architektur machen.


class LinkUser(ABC):
    """Abstract parent class for all kinds link-users."""

    @abstractmethod
    def can_navigate_from_start(self, link) -> bool:
        """
        Indicates, whether the link-user is permitted to use the specified link from the start-node to the end-node.
        :param link: a Link-Object
        :return: bool
        """
        pass

    @abstractmethod
    def can_navigate_to_start(self, link) -> bool:
        """
        Indicates, whether the link-user is permitted to use the specified link from the end-node to the start-node.
        :param link: a Link-Object
        :return: bool
        """
        pass


# Todo(14.11.2019, Lukas Felzmann, Idee von Kai): Man könnte tags wie "cycleway:left" aufteilen in eine Liste [
#  cycleway, left]. Sprich: self__tags wäre kein gewöhnliches Dictionary mehr. Dann könnten wir regeln für
#  solcheFälle definieren und nur noch danach fragen, ob irgendein cycleway-tag vorhanden ist. Das ist relevant
#  füris_navigatable_from_start() und is_navigatable_to_start().


class Pedestrian(LinkUser):
    """Class representing a Pedestrian as a link-user."""

    def can_navigate_from_start(self, link) -> bool:

        if self._may_use(link):

            rules = [link.get_tags().get("oneway:foot") != "-1"]
            if True in rules:
                return True
            else:
                return False

            # So war es vorher:
            # oneway_foot_val = link.get_tags().get("oneway:foot")
            # if oneway_foot_val != "-1":
            #     return True
            # else:
            #     return False

        else:
            return False

    def can_navigate_to_start(self, link) -> bool:
        if self._may_use(link):

            rules = [link.get_tags().get("oneway:foot") != "yes"]
            if True in rules:
                return True
            else:
                return False

            # So war es vorher:
            # oneway_foot_val = link.get_tags().get("oneway:foot")
            # if oneway_foot_val != "yes":
            #     return True
            # else:
            #     return False

        else:
            return False

    def _may_use(self, link) -> bool:

        tags = link.get_tags()
        highway_val = tags.get("highway")
        foot_val = tags.get("foot")
        sidewalk_val = tags.get("sidewalk")
        rules = [highway_val is not None and highway_val in {"residential", "living_street", "bridleway", "path"} and
                 foot_val != "no", highway_val is not None and highway_val in {"pedestrian", "footway", "steps"},
                 sidewalk_val in {"both", "left", "right"} and foot_val not in {None, "no"}, foot_val in {"yes", "designated", "permissive"}]

        if True in rules:
            return True
        else:
            return False

        # So war es vorher:
        # tags = link.get_tags()
        # highway_val = tags.get("highway")
        # foot_val = tags.get("foot")
        #
        # if highway_val is not None:
        #     if highway_val in {"residential", "living_street", "bridleway", "path"}:
        #         if foot_val != "no":
        #             return True
        #
        #     elif highway_val in {"pedestrian", "footway", "steps"}:
        #         return True
        #
        # sidewalk_val = tags.get("sidewalk")
        # if sidewalk_val in {"both", "left", "right"}:
        #     if foot_val not in {None, "no"}:
        #         return True
        #
        # if foot_val in {"yes", "designated", "permissive"}:
        #     return True
        #
        # return False


class Cyclist(LinkUser):
    """Class representing a Cyclist as a link-user."""

    def can_navigate_from_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            oneway_val = tags.get("oneway")
            oneway_bicycle_val = tags.get("oneway:bicycle")
            rules = [oneway_bicycle_val is None and oneway_val != "-1", oneway_bicycle_val not in {None, "-1"}]

            if True in rules:
                return True
            else:
                return False

            # So war es vorher:
            # tags = link.get_tags()
            # oneway_val = tags.get("oneway")
            # oneway_bicycle_val = tags.get("oneway:bicycle")
            #
            # if oneway_bicycle_val is None:
            #     if oneway_val != "-1":
            #         return True
            #     else:
            #         return False
            # else:
            #     if oneway_bicycle_val != "-1":
            #         return True
            #     else:
            #         return False

        else:
            return False

    def can_navigate_to_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            oneway_val = tags.get("oneway")
            oneway_bicycle_val = tags.get("oneway:bicycle")
            rules = [oneway_bicycle_val is None and oneway_val != "yes", oneway_bicycle_val not in {None, "yes"}]

            if True in rules:
                return True
            else:
                return False

            # So war es vorher:
            # tags = link.get_tags()
            # oneway_val = tags.get("oneway")
            # oneway_bicycle_val = tags.get("oneway:bicycle")
            #
            # if oneway_bicycle_val is None:
            #     if oneway_val != "yes":
            #         return True
            #     else:
            #         return False
            # else:
            #     if oneway_bicycle_val != "yes":
            #         return True
            #     else:
            #         return False

        else:
            return False

    def _may_use(self, link) -> bool:

        tags = link.get_tags()

        highway_val = tags.get("highway")
        bicycle_val = tags.get("bicycle")

        rules = [bicycle_val != "no" and highway_val is not None and (highway_val in {"residential", "cycleway", "bridleway", "path"} or (highway_val == "steps" and tags.get("ramp:bicycle") == "yes")),
                 bicycle_val not in {"no", None} and bicycle_val in {"yes", "designated", "use_sidepath", "permissive", "destination"},
                 tags.get("cycleway") not in {None, "no"}, tags.get("bicycle_road") == "yes",
                 tags.get("cyclestreet") == "yes", tags.get("cycleway:right") is not None or tags.get("cycleway:left")
                 is not None or tags.get("cycleway:both") is not None]

        if True in rules:
            return True
        else:
            return False


        # So war es vorher:
        # tags = link.get_tags()
        #
        # highway_val = tags.get("highway")
        # bicycle_val = tags.get("bicycle")
        #
        # if bicycle_val == "no":
        #     return False
        #
        # if highway_val is not None:
        #
        #     if highway_val in {"residential", "cycleway", "bridleway", "path"}:
        #         return True
        #
        #     elif highway_val == "steps":
        #         if tags.get("ramp:bicycle") == "yes":
        #             return True
        #
        # if bicycle_val is not None:
        #     if bicycle_val in {"yes", "designated", "use_sidepath", "permissive", "destination"}:
        #         return True
        #
        # if tags.get("cycleway") not in {None, "no"}:
        #     return True
        #
        # if tags.get("bicycle_road") == "yes":
        #     return True
        #
        # if tags.get("cyclestreet") == "yes":
        #     return True
        #
        # if tags.get("cycleway:right") is not None or tags.get(
        #         "cycleway:left") is not None or tags.get("cycleway:both") is not None:
        #     return True
        #
        # return False


class Car(LinkUser):
    """Class representing a Car as a link-user."""

    def can_navigate_from_start(self, link) -> bool:
        if self._may_use(link):

            oneway_val = link.get_tags().get("oneway")
            rules = [oneway_val != "-1"]

            if True in rules:
                return True
            else:
                return False

            # So war es vorher:
            # oneway_val = link.get_tags().get("oneway")
            # if oneway_val != "-1":
            #     return True
            # else:
            #     return False

        else:
            return False

    def can_navigate_to_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            highway_val = tags.get("highway")
            oneway_val = tags.get("oneway")

            # Todo (13.11.2019, Lukas Felzmann): Nochmal sicherstellen (durch Recherche), ob highway=motorway
            #  auch wirklich nicht zusammen mit oneway=no oder oneway=-1 verwendet wird/werden kann.
            rules = [highway_val != "motorway" and (highway_val != "trunk" or oneway_val in {"no", "-1"}) and oneway_val != "yes"]

            if True in rules:
                return True
            else:
                return False


            # So war es vorher:
            # tags = link.get_tags()
            # highway_val = tags.get("highway")
            # oneway_val = tags.get("oneway")
            #
            # if highway_val == "motorway":
            #     # Todo (13.11.2019, Lukas Felzmann): Nochmal sicherstellen (durch Recherche), ob highway=motorway
            #     #  auch wirklich nicht zusammen mit oneway=no oder oneway=-1 verwendet wird/werden kann.
            #     return False
            # elif highway_val == "trunk" and oneway_val not in {"no", "-1"}:
            #     return False
            #
            # if oneway_val == "yes":
            #     return False
            #
            # return True

        else:
            return False

    def _may_use(self, link) -> bool:

        tags = link.get_tags()
        highway_val = tags.get("highway")
        motor_vehicle_val = tags.get("motor_vehicle")
        motorcar_val = tags.get("motorcar")
        rules = [highway_val is not None and highway_val in {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"},
                 highway_val is not None and highway_val in {"unclassified", "residential", "living_street"} and motor_vehicle_val != "no" and motorcar_val != "no",
                 motor_vehicle_val == "yes" or motorcar_val == "yes"]

        if True in rules:
            return True
        else:
            return False

        # So war es vorher:
        # tags = link.get_tags()
        # highway_val = tags.get("highway")
        # motor_vehicle_val = tags.get("motor_vehicle")
        # motorcar_val = tags.get("motorcar")
        #
        # if highway_val is not None:
        #     if highway_val in {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link",
        #                        "primary_link", "secondary_link", "tertiary_link"}:
        #         return True
        #     elif highway_val in {"unclassified", "residential",
        #                          "living_street"} and motor_vehicle_val != "no" and motorcar_val != "no":
        #         return True
        #
        # if motor_vehicle_val == "yes" or motorcar_val == "yes":
        #     return True
        #
        # return False
