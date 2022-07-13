"""
relational clustering
"""


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
        self.dist = 0
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


def cluster(data: dict):
    """
    :param data: dict of following format:
        {
            'A': ['B', 'C', 'D'],
            'B': ['C', 'D'],
            'C': ['A', 'B']
            ....
        }
    :return: list of points
    """

    # get combinations of all points
    # satisfies:
    # (a, b) == (b, a)

    # first throw all points into one list
    all_points = set(list(data.keys()))
    for points in data.values():
        for point in points:
            all_points.add(point)

    # create all relations
    all_points = list(all_points)
    relations = []

    for i in range(len(all_points)):
        for j in range(i + 1, len(all_points)):
            if all_points[i] != all_points[j]:
                relations.append(Relation(all_points[i], all_points[j]))

    # first calculate distances between all points
    for r in relations:
        # x follows y connection +1
        # y follows x connection +1
        # => 0 == no connection
        # => 1 == weak connection
        # => 2 == strong connection
        if r.b in data and r.a in data[r.b]:
            r.connection += 1
        if r.a in data and r.b in data[r.a]:
            r.connection += 1

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
            r.dist = 1 / r.dist

        # strong connection means even less distance between points
        r.dist *= 1 / (r.connection + 1)

    # now we have all points and all distances they should have from each other
    # cluster them in a 2d image
    # not all distances can be satisfied
    # start with putting base point at (0, 0)



    return relations


# when plotting, strong connections should have another color than weak connections


if __name__ == '__main__':
    # create sample data and test algorithm
    data = {
        'A': ['B', 'C', 'D'],
        'B': ['C', 'D'],
        'C': ['A', 'B']
    }

    print(cluster(data))
