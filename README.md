# Path Searching Visualizer with Pygame

![Path Searching Visualizer]

This is a Python application built using the Pygame library to visualize various pathfinding algorithms. You can use this visualizer to see how different algorithms, such as Breadth-First Search (BFS), Depth-First Search (DFS), Greedy Best-First Search, and A* Search, find paths from a start point to an end point on a grid.

## Features

- Supports multiple pathfinding algorithms: BFS, DFS, Greedy Best-First Search, and A* Search.
- Click to set the start and end points on the grid.
- Use the spacebar to start the pathfinding process.
- Use the right shift key to reset the grid and clear the path.

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/path-searching-visualizer.git
   ```

2. Make sure you have Python 3.x and Pygame installed. If you don't have Pygame, you can install it using pip:

   ```bash
   pip install pygame
   ```

3. Navigate to the project directory:

   ```bash
   cd path-searching-visualizer
   ```

4. Run the visualizer:

   ```bash
   python main.py
   ```

## Usage

- Left-click on any cell to set it as the start point.
- Left-click on another cell to set it as the end point.
- Press the spacebar to start the selected pathfinding algorithm.
- Press the right shift key to reset the grid and clear the path.

## Algorithms

This visualizer supports the following pathfinding algorithms:

- **Breadth-First Search (BFS):** Explores all possible paths in a breadthward motion.

- **Depth-First Search (DFS):** Explores as far as possible along one branch before backtracking.

- **Greedy Best-First Search:** Chooses the path that looks most promising according to a heuristic.

- **A* Search:** Combines the advantages of both BFS and Greedy Best-First Search by considering both the cost to reach the current node and the estimated cost to reach the goal.


## Acknowledgments

This project was inspired by a love for pathfinding algorithms and Pygame. Thanks to the Pygame community and the developers of various pathfinding algorithms for their valuable contributions.
