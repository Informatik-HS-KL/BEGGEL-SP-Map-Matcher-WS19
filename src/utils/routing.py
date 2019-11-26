from abc import ABC

from src import CONFIG
from src.models.link import Link
from src.models.link_user import LinkUser


class WeightCalculator(ABC):
    def get_wight(self, link: Link, fraction=1.0):
        pass


class ShortestPath(WeightCalculator):
    def get_wight(self, link: Link, fraction=1.0):
        return link.get_length() * fraction


# class FastestPath(WeightCalculator):
#     def get_wight(self, link: Link, fraction=1.0):
#         return (link.get_speed_limit()*1000) / link.get_length() * fraction


def point_to_point_dijkstra(initial, end):
    """
    This is a Base Implementation of the Dijkstra Implementation adapted to the Map Service Link, Node Graph.

    :param initial: The start Link
    :param end: The end Link
    :return: List with Nodes from start to end.
             if no Route possible a Error message
    """
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous node, weight)

    initial = initial.get_start_node()
    end = end.get_end_node()

    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        print(current_node.get_id().geohash)
        visited.add(current_node)
        destinations = [link.get_end_node() for link in current_node.get_links()] + [link.get_start_node() for link in
                                                                                     current_node.get_links()]
        destinations = list(filter(lambda n: n != current_node, list(destinations)))
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            # node.get_parent_link().get(weight_prop) # "length" as weigh factor
            weight = 1 + weight_to_current_node  # graph.get[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}

        if not next_destinations:
            raise Exception("Route Not Possible")
        # next node is the destination with the lowest weight
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
        print(current_node)
    # Reverse path
    path = path[::-1]

    return path


def link_to_link_dijkstra(initial, end_link, weight_function: WeightCalculator()):
    """
    This is a Implementation of the Dijkstra Implementation adapted to the Map Service Link, Node Graph.
    The implementation uses links to route
    :param initial: The start Link
    :param end_link: The end Link
    :param weight_function: function to get the weight of an link
    :return: List with Nodes from start to end.
             if no Route possible a Error message
    """
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous link, weight)
    shortest_paths = {initial: (None, 0)}
    current_link = initial
    visited = set()

    while current_link != end_link:
        visited.add(current_link)
        destinations = [link for link in current_link.get_links_at_start_node()] + \
                       [link for link in current_link.get_links_at_end_node()]

        destinations = list(filter(lambda n: n != current_link, list(destinations)))
        weight_to_current_node = shortest_paths[current_link][1]

        for next_link in destinations:
            weight = weight_function.get_wight(next_link) + weight_to_current_node
            if next_link not in shortest_paths:
                shortest_paths[next_link] = (current_link, weight)
            else:
                current_shortest_weight = shortest_paths[next_link][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_link] = (current_link, weight)

        next_destinations = {link: shortest_paths[link] for link in shortest_paths if link not in visited}

        if not next_destinations:
            raise Exception("Route Not Possible")
        # next link is the destination with the lowest weight
        current_link = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_link is not None:
        path.append(current_link.get_start_node())
        next_link = shortest_paths[current_link][0]
        current_link = next_link
        print(current_link)
    # Reverse path
    path = path[::-1]

    return path


def dijkstra_routing(start_link, start_fraction, end_link, end_fraction, weight_function, from_start_to_end,
                     link_user: LinkUser):
    """
    This Dijkstra also takes into account route options such as one-way streets
    Default a list of all start Nodes will return if no possible  route it returns a Error String

    :param start_link:
    :param start_fraction:
    :param end_link:
    :param end_fraction:
    :param weight_function:
    :param from_start_to_end:
    :param link_user:
    :return:
    """
    if start_link == end_link:
        return [start_link.get_start_node(), start_link.get_end_node()]

    start_length = weight_function.get_wight(start_link, (start_fraction if from_start_to_end else 1 - start_fraction))
    possible_ways = [(start_length, [start_link])]
    already_used = {start_link}

    if from_start_to_end:
        __update_first_way(possible_ways, start_link.get_links_at_end_node(link_user), weight_function, already_used)
    else:
        __update_first_way(possible_ways, start_link.get_links_at_start_node(link_user), weight_function, already_used)
    i = 0
    while i < CONFIG.getint("DEFAULT", "max_dijkstra_iterations"):
        i = i + 1
        if len(possible_ways) == 0:
            return Exception("Route Not Possible")
        possible_ways = sorted(possible_ways, key=lambda pw: pw[0])
        destinations = [link for link in possible_ways[0][1][-1].get_links_at_start_node(link_user)] + \
                       [link for link in possible_ways[0][1][-1].get_links_at_end_node(link_user)]

        if end_link in destinations:
            print(i)
            shortest_way = possible_ways[0][1][:]
            shortest_way.append(end_link)
            list_nodes = []
            for link in shortest_way:
                list_nodes.append(link.get_start_node())
            return list_nodes

        __update_first_way(possible_ways, destinations, weight_function, already_used)


def __update_first_way(possible_ways: list, next_links: list, weight_function, already_used: set):
    """
    This function add the neu Links for the first (shortest) way in possible_ways
    After the neu ways are inserted, the first way will dropped

    :param possible_ways: List with all traveled routes and their weight
    :param next_links: List of all accessible routes from the first route in possible_ways
    :param weight_function: function to calculate the Link weight
    :param already_used: List with all already traveled links
    :return:
    """
    for link in next_links:
        if link in already_used:
            continue
        new_way = possible_ways[0][1][:]
        new_way.append(link)
        already_used.add(link)
        possible_ways.append((possible_ways[0][0] + weight_function.get_wight(link), new_way))

    del possible_ways[0]
