# Dijkstra Backpack Problem Solver

A web application that solves the Knapsack Problem using Dijkstra's algorithm with a user-friendly interface built with Flask.

## Live Demo

This application is hosted and available at: https://dijkstra-backpack-problem.onrender.com/

## Problem Description

The Knapsack Problem is a classic optimization challenge where you have:
- A set of items, each with a volume and a value
- A backpack with a maximum capacity

The goal is to select items to maximize the total value while keeping the total volume under the backpack's capacity.

## Dijkstra's Algorithm Approach

While Dijkstra's algorithm is typically used for finding the shortest paths in graphs, this project adapts it to solve the Knapsack Problem by:

1. Representing the problem as a graph where:
   - Vertices are states (remaining capacity, current item)
   - Edges represent decisions (take or skip an item)
   - Edge weights are derived from item values

2. Finding the optimal path through this graph to determine which items to include.

## Features

- Web-based interface for entering problem parameters
- Real-time input validation
- Detailed error handling
- Interactive graph visualization
- Random data generation
- Responsive design

## Project Structure

```
Dijkstra-Bacpack-Problem/
├── algorithm/
│   └── dijkstra.py        # Core algorithm implementation
├── static/
│   ├── script.js          # Frontend JavaScript for validation and interaction
│   ├── style.css          # CSS styling for main page
│   ├── style_error_template.css # CSS styling for error page
│   ├── favicon.png        # Favicon image
│   ├── info.png           # Information button icon
│   └── results.png        # Results button icon
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
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:8080`

3. Enter the problem parameters:
   - Values: Comma-separated numbers representing item values (e.g., "10,20,15,30,5")
   - Volumes: Comma-separated numbers representing item volumes (e.g., "1,2,4.5,23.8,0.5")
   - Capacity: Maximum capacity of the backpack (e.g., "30")

4. Click "Solve" to get the optimal solution
   
5. Click on the "Results" icon to see a summary of the selected items

## Graph Visualization

The solution is visualized as a graph where:
- Gray nodes: Possible configurations not in the optimal solution
- Green nodes: Nodes in the optimal path
- Orange nodes: Items included in the optimal solution
- Red nodes: Start and end nodes of the backpack graph

## Algorithm Details

The implementation uses a graph-based approach:

1. Each vertex in the graph represents a state (remaining capacity, current item index)
2. From each vertex, we have two possible transitions:
   - Skip the current item (no change in capacity)
   - Take the current item (reduce capacity by item's volume)
3. Dijkstra's algorithm finds the shortest path from the initial state to the final state
4. The path determines which items to include in the backpack

## Example

For a backpack with capacity 5 and items:
- Item 1: volume 1, value 60
- Item 2: volume 2, value 100
- Item 3: volume 3, value 120

The optimal solution is to take items 2 and 3, yielding a total value of 220.
