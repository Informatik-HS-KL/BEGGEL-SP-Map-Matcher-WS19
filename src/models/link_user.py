from abc import ABC, abstractmethod


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


class Pedestrian(LinkUser):
    """Class representing a Pedestrian as a link-user."""

    def can_navigate_from_start(self, link) -> bool:

        if self._may_use(link):

            rules = [link.get_tags().get("oneway:foot") != "-1"]
            return True in rules

        else:
            return False

    def can_navigate_to_start(self, link) -> bool:
        if self._may_use(link):

            rules = [link.get_tags().get("oneway:foot") != "yes"]
            return True in rules

        else:
            return False

    def _may_use(self, link) -> bool:
        """
        :param link: Link-Object
        :return:
        """
        tags = link.get_tags()
        highway_val = tags.get("highway")
        foot_val = tags.get("foot")
        sidewalk_val = tags.get("sidewalk")
        rules = [highway_val is not None and highway_val in {"residential", "living_street", "bridleway", "path"}
                 and foot_val != "no",
                 highway_val is not None and highway_val in {"pedestrian", "footway", "steps"},
                 sidewalk_val in {"both", "left", "right"} and foot_val not in {None, "no"},
                 foot_val in {"yes", "designated", "permissive"}]

        return True in rules

class Cyclist(LinkUser):
    """Class representing a Cyclist as a link-user."""

    def can_navigate_from_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            oneway_val = tags.get("oneway")
            oneway_bicycle_val = tags.get("oneway:bicycle")
            rules = [oneway_bicycle_val is None and oneway_val != "-1",
                     oneway_bicycle_val not in {None, "-1"}]

            return True in rules
        else:
            return False

    def can_navigate_to_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            oneway_val = tags.get("oneway")
            oneway_bicycle_val = tags.get("oneway:bicycle")
            rules = [oneway_bicycle_val is None and oneway_val != "yes",
                     oneway_bicycle_val not in {None, "yes"}]

            return True in rules
        else:
            return False

    def _may_use(self, link) -> bool:
        """
        :param link: Link Object
        :return:
        """
        tags = link.get_tags()

        highway_val = tags.get("highway")
        bicycle_val = tags.get("bicycle")

        rules = [bicycle_val != "no" and highway_val is not None and (highway_val in {"residential", "cycleway", "bridleway", "path"} or (highway_val == "steps" and tags.get("ramp:bicycle") == "yes")),
                 bicycle_val not in {"no", None} and bicycle_val in {"yes", "designated", "use_sidepath", "permissive", "destination"},
                 tags.get("cycleway") not in {None, "no"},
                 tags.get("bicycle_road") == "yes",
                 tags.get("cyclestreet") == "yes",
                 tags.get("cycleway:right") is not None or tags.get("cycleway:left") is not None or tags.get("cycleway:both") is not None]


        return True in rules


class Car(LinkUser):
    """Class representing a Car as a link-user."""

    def can_navigate_from_start(self, link) -> bool:
        if self._may_use(link):

            oneway_val = link.get_tags().get("oneway")
            rules = [oneway_val != "-1"]

            return True in rules

        else:
            return False

    def can_navigate_to_start(self, link) -> bool:

        if self._may_use(link):

            tags = link.get_tags()
            highway_val = tags.get("highway")
            oneway_val = tags.get("oneway")

            rules = [highway_val != "motorway" and (highway_val != "trunk" or oneway_val in {"no", "-1"}) and oneway_val != "yes"]

            return True in rules

        else:
            return False

    def _may_use(self, link) -> bool:
        """
        :param link: Link-Object
        :return:
        """
        tags = link.get_tags()
        highway_val = tags.get("highway")
        motor_vehicle_val = tags.get("motor_vehicle")
        motorcar_val = tags.get("motorcar")
        rules = [highway_val is not None and highway_val in {"motorway", "trunk", "primary", "secondary", "tertiary", "motorway_link", "trunk_link", "primary_link", "secondary_link", "tertiary_link"},
                 highway_val is not None and highway_val in {"unclassified", "residential", "living_street"} and motor_vehicle_val != "no" and motorcar_val != "no",
                 motor_vehicle_val == "yes" or motorcar_val == "yes"]


        return True in rules
