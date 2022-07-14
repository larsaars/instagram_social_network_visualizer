#!/usr/bin/env python3
"""
use loaded network and tools in relational_clustering.py
save weighted edges to file
"""

from relational_clustering import find_edges_and_weights
from pandas import DataFrame
import json

if __name__ == '__main__':
    # load .json file
    with open('followings.json', 'r') as f:
        all_followings = json.load(f)

    # find edges and weights
    edges = find_edges_and_weights(all_followings)
    # create pandas dataframe
    edge_df = DataFrame(edges, columns=['Source', 'Target', 'Weight'])
    # save csv
    edge_df.to_csv('edges.csv')

    # can be imported in a software like Gephi
    # Gephi tutorial: https://www.youtube.com/watch?v=HJ4Hcq3YX4k
    # for labels copy in node table the id values to Label values
    # let OpenOrd run as algorithm and then Expand mutliple times

