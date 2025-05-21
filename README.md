# Dijkstra Backpack Problem Solver

A web application that solves the Knapsack Problem using Dijkstra's algorithm with a user-friendly interface built with Flask.

## Problem Description

The Knapsack Problem is a classic optimization challenge where you have:
- A set of items, each with a weight and a value
- A knapsack with a maximum weight capacity

The goal is to select items to maximize the total value while keeping the total weight under the knapsack's capacity.

## Dijkstra's Algorithm Approach

While Dijkstra's algorithm is typically used for finding shortest paths in graphs, this project adapts it to solve the Knapsack Problem by:

1. Representing the problem as a graph where:
   - Vertices are states (remaining capacity, current item)
   - Edges represent decisions (take or skip an item)
   - Edge weights are derived from item values

2. Finding the optimal path through this graph to determine which items to include.

## Features

- Web-based interface for entering problem parameters
- Real-time input validation
- Detailed error handling
- Visualization of results
- Responsive design

## Project Structure

```
Dijkstra-Bacpack-Problem/
├── algorithm/
│   └── dijkstra.py        # Core algorithm implementation
├── static/
│   ├── script.js          # Frontend JavaScript for validation
│   └── style.css          # CSS styling
├── templates/
│   ├── index.html         # Main input form
│   └── error-template.html # Error page template
└── app.py                 # Flask application
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/SzyMm0n/Dijkstra-Bacpack-Problem.git
   cd Dijkstra-Bacpack-Problem
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install flask
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:8080`

3. Enter the problem parameters:
   - Weights: Comma-separated numbers (e.g., "1,2,4.5,23.8,0.5")
   - Values: Comma-separated numbers (e.g., "10,20,15,30,5")
   - Capacity: Maximum weight capacity (e.g., "30")

4. Click "Solve" to get the optimal solution

## Algorithm Details

The implementation uses a graph-based approach:

1. Each vertex in the graph represents a state (remaining capacity, current item index)
2. From each vertex, we have two possible transitions:
   - Skip the current item (no change in capacity)
   - Take the current item (reduce capacity by item's weight)
3. Dijkstra's algorithm finds the shortest path from the initial state to the final state
4. The path determines which items to include in the knapsack

## Example

For a knapsack with capacity 5 and items:
- Item 1: weight 1, value 60
- Item 2: weight 2, value 100
- Item 3: weight 3, value 120

The optimal solution is to take items 2 and 3, yielding a total value of 220.
