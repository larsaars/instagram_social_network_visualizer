"""
relational clustering
"""

from tqdm import tqdm


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
    name_from_id = {k: v for k, v in enumerate(all_points)}
    id_from_name = {v: k for k, v in name_from_id.items()}  # reverse dict

    # replace everything in data dict with ids
    id_data = dict()
    for key in data:
        id_data[id_from_name[key]] = [id_from_name[name] for name in data[key]]

    print('Removing all single points (just one relation)...')
    # remove points that are just themselves (no relation)
    # they are overhead in the graph and are not interesting
    # they also take up a lot of computing time
    all_points = []
    for point in name_from_id.keys():
        # count occurrences
        count = 0
        for points in id_data.values():
            if point in points:
                count += 1

        # if there is only one occurrence, it is not a point
        if count > 1:
            all_points.append(point)

    # the final edges of the graph
    # look like this:
    # (name a, name b, weight)
    edges = []

    print('Creating relations and calculating edges from these...')
    for i in tqdm(range(len(all_points))):
        for j in range(i + 1, len(all_points)):
            if all_points[i] != all_points[j]:
                # create relation object
                a, b = all_points[i], all_points[j]
                # x follows y connection +1
                # y follows x connection +1
                # => 0 == no connection
                # => 1 == weak connection
                # => 2 == strong connection
                connection = 0
                if b in id_data and a in id_data[b]:
                    connection += 1
                if a in id_data and b in id_data[a]:
                    connection += 1

                if connection > 0:
                    # (x, y) == (y, x)
                    # loop through all points c
                    # if a follows c and b follows c
                    # => dist += 1
                    # meaning: a and b both follow c -> they are both in the same network
                    dist = 0
                    for c in all_points:
                        if a in id_data and c in id_data[a] and b in id_data and c in id_data[b]:
                            dist += 1

                    # they both follow the same persons:
                    # distance should be smaller
                    # => dist = 1 / dist
                    if dist == 0:
                        dist = 2
                    else:
                        dist = 1 / (dist ** 1.4)

                    # strong connection means even less distance between points
                    dist *= 1 / (connection + 1)

                    # add to edge list
                    # decrypt ids to names again
                    edges.append((name_from_id[a], name_from_id[b], dist))

    # return final edges
    return edges


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
