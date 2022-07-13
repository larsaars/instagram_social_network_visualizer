#!/usr/bin/env python3
"""
use loaded network and tools in relational_clustering.py
save weighted edges to file
"""

import json
from relational_clustering import find_edges_and_weights

if __name__ == '__main__':
    # load .json file
    with open('followings.json', 'r') as f:
        all_followings = json.load(f)

    # find edges and weights
    edges = find_edges_and_weights(all_followings)

    # save edges to file
    with open('edges.json', 'w') as f:
        json.dump(edges, f)

