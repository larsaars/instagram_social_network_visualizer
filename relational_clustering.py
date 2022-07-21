"""
relational clustering
"""

from tqdm import tqdm
import pandas as pd


def find_nodes_and_edges(data: dict, min_num_of_relations=2, edges_path='./results/edges.csv',
                         nodes_path='./results/nodes.csv'):
    """
    :param edges_path: path to edges file
    :param nodes_path: path to nodes file
    :param min_num_of_relations: minimum number of relations between data points to be considered as interconnected
    :param data: dict of following format:
        {
            'A': ['B', 'C', 'D'],
            'B': ['C', 'D'],
            'C': ['A', 'B']
            ....
        }
    """

    print('Finding all nodes...')

    # first throw all points into one list
    all_nodes = set(list(data.keys()))
    for points in data.values():
        for point in points:
            all_nodes.add(point)

    print(f'Creating ids for nodes (highest id: {len(all_nodes) - 1})')

    # create all relations
    # create ids for names
    # comparing numbers is faster than comparing strings
    id_from_name = {k: v for v, k in enumerate(all_nodes)}
    name_from_id = {v: k for k, v in id_from_name.items()}  # reverse dict

    # replace everything in data dict with ids
    id_data = dict()
    for key in data:
        id_data[id_from_name[key]] = [id_from_name[name] for name in data[key]]

    print('Removing all single nodes not fulfilling constraints (min num of relations)...')
    # remove points that are just themselves (no relation)
    # they are overhead in the graph and are not interesting
    # they also take up a lot of computing time
    all_nodes = []
    for node in id_from_name.values():
        # count occurrences
        count = 0
        for nodes in id_data.values():
            if node in nodes:
                count += 1

        # if there is only one occurrence, it is not a point
        if count >= min_num_of_relations:
            all_nodes.append(node)

    # the final edges of the graph
    # look like this:
    # (name a, name b, weight)
    edges = []

    print('Calculating edges and relations...')
    for i in tqdm(range(len(all_nodes))):
        for j in range(i + 1, len(all_nodes)):
            if all_nodes[i] != all_nodes[j]:
                # create relation object
                a, b = all_nodes[i], all_nodes[j]
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
                    # add to edge list (as ids)
                    edges.append((a, b, connection))

    # save edges and names (nodes) to file
    print('Saving edges and nodes to file...')

    # create pandas dataframes and save them
    pd.DataFrame(edges, columns=['Source', 'Target', 'Weight']) \
        .to_csv(edges_path, index=False)
    pd.DataFrame([(node_id, name_from_id[node_id]) for node_id in all_nodes], columns=['Id', 'Label']) \
        .to_csv(nodes_path, index=False)

    print('Done! Can be imported in Gephi.')


if __name__ == '__main__':
    # create sample data and test algorithm
    data = {
        'A': ['B', 'C', 'D'],
        'B': ['C', 'D'],
        'C': ['A', 'B'],
        'Epsilon': ['Faa', 'Gaa', 'A'],
    }

    find_nodes_and_edges(data)
