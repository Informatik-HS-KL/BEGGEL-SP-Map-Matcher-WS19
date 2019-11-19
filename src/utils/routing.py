from abc import ABC
from src.models.link import Link


class WeightCalculator(ABC):
    def get_wight(self, link: Link, fraction=1.0):
        pass


class ShortestPath(WeightCalculator):
    def get_wight(self, link: Link, fraction=1.0):
        return link.get_length() * fraction


class FastestPath(WeightCalculator):
    def get_wight(self, link: Link, fraction=1.0):
        return link.get_length() * fraction


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
            return "Route Not Possible"
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
    # shortest paths is a dict of nodes
    # whose value is a tuple of (previous link, weight)
    print("EXECUTE FUNKTION link_to_link_dijkstra")
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
            return "Route Not Possible"
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

def test_dijkstra(initial, initial_fraction, end_link, end_fraction, weight_function, from_start_to_end):

    if from_start_to_end:
        initial.get_links_at_end_node()
    else:
        initial.get_links_at_start_node()