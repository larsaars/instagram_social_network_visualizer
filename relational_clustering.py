"""
relational clustering
"""

import matplotlib.pyplot as plt
import networkx as nx


class Relation(object):
    """
    Relation class

    (a, b) == (b, a)

    dist distance between x and y

    connection 0 if x and y are not connected
    connection 1 if x and y are connected
    connection 2 if x and y and y and x are connected
    """

    def __init__(self, a, b):
        # nominators
        self.a = a
        self.b = b
        # distance between a and b
        self.dist = 1
        # type of connection (weak or strong or none)
        self.connection = 0
        # final coordinates of a and b
        self.x = 0
        self.y = 0

    def __str__(self):
        return f'({self.a}, {self.b})'

    def __repr__(self):
        return f'({self.a}, {self.b}, {self.dist}, {self.connection})'

    def __eq__(self, other):
        return (self.a == other.a and self.b == other.b) or \
               (self.a == other.b and self.b == other.a)

    def __hash__(self):
        return hash(str(self))


def find_edges_and_weights(data: dict):
    """
    :param data: dict of following format:
        {
            'A': ['B', 'C', 'D'],
            'B': ['C', 'D'],
            'C': ['A', 'B']
            ....
        }
    :return: list of edges and weights
    """

    # get combinations of all points
    # satisfies:
    # (a, b) == (b, a)

    print('Finding all points...')

    # first throw all points into one list
    all_points = set(list(data.keys()))
    for points in data.values():
        for point in points:
            all_points.add(point)

    print(f'Creating ids (highest id: {len(all_points) - 1})')

    # create all relations
    # create ids for names
    # comparing numbers is faster than comparing strings
    ids = {k: v for k, v in enumerate(all_points)}

    # all_points is a list of the keys
    all_points = list(ids.keys())
    relations = []

    print('Creating relations...')
    for i in range(len(all_points)):
        for j in range(i + 1, len(all_points)):
            if all_points[i] != all_points[j]:
                # create relation object
                r = Relation(all_points[i], all_points[j])
                # x follows y connection +1
                # y follows x connection +1
                # => 0 == no connection
                # => 1 == weak connection
                # => 2 == strong connection
                if r.b in data and r.a in data[r.b]:
                    r.connection += 1
                if r.a in data and r.b in data[r.a]:
                    r.connection += 1

                if r.connection > 0:
                    relations.append(r)

    # the final edges of the graph
    # look like this:
    # (name a, name b, weight)
    edges = []

    print('Calculating edges and distances...')

    # first calculate distances between all points
    for r in relations:
        # (x, y) == (y, x)
        # loop through all points c
        # if a follows c and b follows c
        # => dist += 1
        # meaning: a and b both follow c -> they are both in the same network
        for c in all_points:
            if r.a in data and c in data[r.a] and r.b in data and c in data[r.b]:
                r.dist += 1

        # they both follow the same persons:
        # distance should be smaller
        # => dist = 1 / dist
        if r.dist == 0:
            r.dist = 2
        else:
            r.dist = 1 / (r.dist ** 1.4)

        # strong connection means even less distance between points
        r.dist *= 1 / (r.connection + 1)

        # add to edge list
        # decrypt ids to names again
        edge = (ids[r.a], ids[r.b], r.dist)
        print(f'Added edge: {edge}')
        edges.append(edge)

    # return final edges
    return edges


def draw_edges(edges: list):
    print('Drawing graph...')

    # create graph
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    # draw the graph (using networkx)
    nx.draw(G, with_labels=True, edge_color='grey', node_size=4, node_color='blue', font_color='black', alpha=0.5,
            width=1)
    plt.show()


if __name__ == '__main__':
    # create sample data and test algorithm
    data = {
        'A': ['B', 'C', 'D'],
        'B': ['C', 'D'],
        'C': ['A', 'B'],
        'Epsilon': ['Faa', 'Gaa', 'A'],
    }

    edges = find_edges_and_weights(data)

    print(edges)
    draw_edges(edges)
