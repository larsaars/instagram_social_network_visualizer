"""
draw the network saved in edges.json
"""

import json
from pandas import DataFrame

if __name__ == '__main__':
    # load .json file
    with open('edges.json', 'r') as f:
        edges = json.load(f)

    edge_df = DataFrame(edges, columns=['from', 'to', 'weight'])

    edge_df.to_csv('edges.csv')
