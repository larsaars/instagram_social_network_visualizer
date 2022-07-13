"""
draw the network saved in edges.json
"""

import json

from relational_clustering import draw_edges

if __name__ == '__main__':
    # load .json file
    with open('edges.json', 'r') as f:
        edges = json.load(f)

    # draw edges
    draw_edges(edges)
