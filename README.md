# Puzzle Game with Search Algorithms

A sliding puzzle game that compares 4 different search algorithms to solve 8-puzzles.

## What It Does

Solves sliding puzzles using 4 search algorithms:
- **Breadth-First Search (BFS)** - Finds optimal solution, explores many nodes
- **Depth-First Search (DFS)** - Fast but may not find solution
- **A* Search** - Smart and efficient, finds optimal solution
- **Greedy Best-First** - Very fast but may find longer solutions

## How to Run

```bash
python puzzle_game.py
```

## What You'll See

1. **Performance Summary** - Compare algorithm speed and efficiency
2. **Step-by-Step Solutions** - Watch how each algorithm solves the puzzle
3. **Two Visualization Modes**:
   - Compact view (side-by-side)
   - Detailed view (vertical)

## Current Puzzle

```
Initial:  [8, 6, 7]    Goal: [1, 2, 3]
          [2, 5, 4]          [4, 5, 6]
          [3, ' ', 1]        [7, 8, ' ']
```

## Customization

- Change puzzle: Edit `create_puzzle()` function
- Adjust DFS depth limit: Modify `max_depth` parameter (currently 50)

## Requirements

Python 3.7+ (uses only standard library modules)

## Example Output

```
Algorithm                 Steps    Nodes      Time (s)   Status
----------------------------------------------------------------------
Breadth-First Search      31       181347     5.9768     ✅ Solved
A* Search                 31       21198      1.1816     ✅ Solved
Greedy Best-First Search  47       83         0.0044     ✅ Solved
Depth-First Search        N/A      30660      0.9802     ❌ Failed
```

**A* is usually the best balance of speed and optimality!**
