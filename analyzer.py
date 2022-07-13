"""
use loaded network and tools in relational_clustering.py
to visualize the network
"""

import json
from relational_clustering import draw_edges, find_edges_and_weights
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # load .json file
    with open('followings.json', 'r') as f:
        all_followings = json.load(f)

    # find edges and weights
    edges = find_edges_and_weights(all_followings)

    # draw edges
    draw_edges(edges)
    plt.show()
