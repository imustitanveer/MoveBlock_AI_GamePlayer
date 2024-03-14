# MoveBlock AI Game Player

This repository contains a simple implementation of the MoveBlock game and various searching algorithms to solve it.

## Problem Definition

The MoveBlock problem consists of the following components:

- Goal Block: The block that needs to reach the goal state.
- Hurdle Blocks: The blocks that are obstacles in the way of the Goal Block.
- Empty Spaces: Spaces where blocks can be moved.

## Environment

The game environment is fully observable and deterministic, represented as a grid. Each block is 1x2 in grid size, either horizontally or vertically.

## Gameplay

- Start with an initial state and a goal state.
- Each move (slide) has a cost of 1.
- Goal test function checks if the goal block is at the goal state.

## Heuristic

The Manhattan distance heuristic can be used for this problem, determining the distance of the goal block from the goal state to make informed search decisions.

## Algorithms

- Breadth First Search (BFS): Explores nodes level by level.
- Uniform Cost Search (UCS): Explores nodes with the lowest cost.
- Depth First Search (DFS): Explores as deeply as possible along each branch.
- Greedy Search: Selects the node with the lowest heuristic value.
- A-Star Search: Selects the node with the lowest total cost.

## Optimal Algorithm

In this problem, BFS and UCS have the same cost and nodes explored. DFS has a low-cost solution but explores the most nodes. Greedy Search has a lower cost than BFS and UCS and explores fewer nodes than DFS, but the heuristic may cause backtracking. A-Star Search would likely reach the same conclusion as Greedy Search, making it complete and optimal.

## Repository

- [GitHub Repository](https://github.com/imustitanveer/MoveBlock_AI_GamePlayer)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/imustitanveer/MoveBlock_AI_GamePlayer.git
   ```

2. Run the main script for the desired algorithm:

   ```bash
   python main.py
   ```

3. Follow the prompts to input the initial and goal states, and the script will output the solution path and cost.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
