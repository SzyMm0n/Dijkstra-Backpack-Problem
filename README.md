# Backpack Dijkstra Problem
This is a simple implementation of the _Dijkstra_ algorithm to solve the backpack problem.

## Problem Statement
The backpack problem is a classic optimization problem where you have a set of items, 
each with a weight and a value, and you want to maximize the total value of the items 
you can carry in a backpack of limited capacity. The Dijkstra algorithm is typically used for finding the shortest paths 
between nodes in a graph, but it can also be adapted to solve the backpack problem by treating items as nodes
and their weights as edges.

## Implementation
The implementation is done in Python and uses the `turtle` library to visualize the algorithm. 

## Graph Representation
The graph is represented as a matrix, where each cell contains the weight and value of an item. The algorithm iterates through the graph,
updating the maximum value that can be carried in the backpack at each step. 