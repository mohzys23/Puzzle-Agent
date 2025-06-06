import heapq
from collections import deque
import time
import copy

class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.size = len(board)
        
    def __eq__(self, other):
        return self.board == other.board
    
    def __hash__(self):
        return hash(str(self.board))
    
    def __lt__(self, other):
        return False  # For heapq when f-values are equal
    
    def get_blank_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return i, j
        return None
    
    def get_neighbors(self):
        neighbors = []
        blank_row, blank_col = self.get_blank_position()
        
        # Possible moves: up, down, left, right
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for dr, dc, move_name in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_board = copy.deepcopy(self.board)
                # Swap blank with adjacent tile
                new_board[blank_row][blank_col] = new_board[new_row][new_col]
                new_board[new_row][new_col] = 0
                
                neighbor = PuzzleState(new_board, self, move_name, self.depth + 1)
                neighbors.append(neighbor)
        
        return neighbors
    
    def manhattan_distance(self, goal_state):
        distance = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    value = self.board[i][j]
                    # Find where this value should be in goal state
                    for gi in range(self.size):
                        for gj in range(self.size):
                            if goal_state.board[gi][gj] == value:
                                distance += abs(i - gi) + abs(j - gj)
                                break
        return distance
    
    def misplaced_tiles(self, goal_state):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0 and self.board[i][j] != goal_state.board[i][j]:
                    count += 1
        return count
    
    def display(self):
        for row in self.board:
            print([x if x != 0 else ' ' for x in row])
        print()

def get_solution_path(state):
    path = []
    current = state
    while current.parent is not None:
        path.append(current.move)
        current = current.parent
    return path[::-1]

def get_solution_states(state):
    """Get all states in the solution path including initial state"""
    states = []
    current = state
    while current is not None:
        states.append(current)
        current = current.parent
    return states[::-1]

def visualize_solution(initial_state, solution_state, algorithm_name):
    """Show step-by-step solution visualization"""
    if solution_state is None:
        print(f"❌ {algorithm_name}: No solution to visualize")
        return
    
    states = get_solution_states(solution_state)
    moves = get_solution_path(solution_state)
    
    print(f"\n🎬 {algorithm_name} - Complete Solution Path:")
    print("=" * 80)
    
    # Show initial state
    print(f"Step 0: Initial")
    states[0].display()
    
    # Show each move with compact display
    for i, move in enumerate(moves):
        print(f"Step {i+1}: {move}")
        states[i+1].display()
    
    print(f"🎉 Solution completed in {len(moves)} steps!")
    print("=" * 80)

def visualize_solution_compact(initial_state, solution_state, algorithm_name):
    """Show compact side-by-side solution visualization"""
    if solution_state is None:
        print(f"❌ {algorithm_name}: No solution to visualize")
        return
    
    states = get_solution_states(solution_state)
    moves = get_solution_path(solution_state)
    
    print(f"\n🎬 {algorithm_name} - Compact Solution ({len(moves)} steps):")
    print("=" * 80)
    
    # Display states in groups of 3 for better readability
    for start_idx in range(0, len(states), 3):
        end_idx = min(start_idx + 3, len(states))
        
        # Print step headers
        step_headers = []
        for idx in range(start_idx, end_idx):
            if idx == 0:
                step_headers.append(f"Step {idx}: Initial".center(20))
            else:
                step_headers.append(f"Step {idx}: {moves[idx-1]}".center(20))
        
        print("  ".join(step_headers))
        
        # Print board rows side by side
        for row in range(3):  # 3x3 puzzle
            row_displays = []
            for idx in range(start_idx, end_idx):
                board_row = str(states[idx].board[row]).replace('0', ' ')
                row_displays.append(board_row.center(20))
            print("  ".join(row_displays))
        
        print()  # Empty line between groups
    
    print("=" * 80)

def breadth_first_search(initial_state, goal_state):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    queue = deque([initial_state])
    visited = {initial_state}
    nodes_expanded = 0
    
    while queue:
        current_state = queue.popleft()
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if neighbor == goal_state:
                path = get_solution_path(neighbor)
                return path, nodes_expanded, len(path), neighbor
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return None, nodes_expanded, 0, None  # No solution found

def depth_first_search(initial_state, goal_state, max_depth=20):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    stack = [initial_state]
    visited = set()
    nodes_expanded = 0
    
    while stack:
        current_state = stack.pop()
        
        if current_state in visited or current_state.depth > max_depth:
            continue
            
        visited.add(current_state)
        nodes_expanded += 1
        
        if current_state == goal_state:
            path = get_solution_path(current_state)
            return path, nodes_expanded, len(path), current_state
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in visited and neighbor.depth <= max_depth:
                stack.append(neighbor)
    
    return None, nodes_expanded, 0, None  # No solution found

def a_star_search(initial_state, goal_state):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    open_list = []
    heapq.heappush(open_list, (0, 0, initial_state))  # (f, g, state)
    visited = set()
    nodes_expanded = 0
    
    while open_list:
        f, g, current_state = heapq.heappop(open_list)
        
        if current_state in visited:
            continue
            
        visited.add(current_state)
        nodes_expanded += 1
        
        if current_state == goal_state:
            path = get_solution_path(current_state)
            return path, nodes_expanded, len(path), current_state
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in visited:
                g_new = current_state.depth + 1
                h = neighbor.manhattan_distance(goal_state)
                f_new = g_new + h
                heapq.heappush(open_list, (f_new, g_new, neighbor))
    
    return None, nodes_expanded, 0, None  # No solution found

def greedy_best_first_search(initial_state, goal_state):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    open_list = []
    heapq.heappush(open_list, (0, initial_state))  # (h, state)
    visited = set()
    nodes_expanded = 0
    
    while open_list:
        h, current_state = heapq.heappop(open_list)
        
        if current_state in visited:
            continue
            
        visited.add(current_state)
        nodes_expanded += 1
        
        if current_state == goal_state:
            path = get_solution_path(current_state)
            return path, nodes_expanded, len(path), current_state
        
        for neighbor in current_state.get_neighbors():
            if neighbor not in visited:
                h_new = neighbor.manhattan_distance(goal_state)
                heapq.heappush(open_list, (h_new, neighbor))
    
    return None, nodes_expanded, 0, None  # No solution found

def create_puzzle():
    # Hard puzzle (many moves to solve)
    initial_board = [
        [8, 6, 7],
        [2, 5, 4],
        [3, 0, 1]
    ]
    
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    return PuzzleState(initial_board), PuzzleState(goal_board)

def run_all_algorithms(initial_state, goal_state):
    algorithms = [
        ("Breadth-First Search", breadth_first_search),
        ("Depth-First Search", depth_first_search),
        ("A* Search", a_star_search),
        ("Greedy Best-First Search", greedy_best_first_search)
    ]
    
    print("Initial State:")
    initial_state.display()
    print("Goal State:")
    goal_state.display()
    print("=" * 50)
    
    results = []
    solution_states = []  # Store solution states for visualization
    
    for name, algorithm in algorithms:
        print(f"\n{name}:")
        start_time = time.time()
        
        if name == "Depth-First Search":
            result = algorithm(initial_state, goal_state, max_depth=50)
        else:
            result = algorithm(initial_state, goal_state)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        path, nodes_expanded, path_length, solution_state = result
        
        if path is not None:
            print(f"✅ Solution found!")
            print(f"Moves: {' -> '.join(path) if path else 'Already solved'}")
            print(f"Path length: {path_length}")
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Time taken: {execution_time:.4f} seconds")
            
            results.append({
                'algorithm': name,
                'solved': True,
                'steps': path_length,
                'nodes': nodes_expanded,
                'time': execution_time,
                'moves': ' -> '.join(path) if path else 'Already solved'
            })
            solution_states.append((name, solution_state))
        else:
            print(f"❌ No solution found within limits")
            print(f"Nodes expanded: {nodes_expanded}")
            print(f"Time taken: {execution_time:.4f} seconds")
            
            results.append({
                'algorithm': name,
                'solved': False,
                'steps': 0,
                'nodes': nodes_expanded,
                'time': execution_time,
                'moves': 'No solution'
            })
            solution_states.append((name, None))
    
    # Print summary table
    print("\n" + "=" * 70)
    print("📊 ALGORITHM PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"{'Algorithm':<25} {'Steps':<8} {'Nodes':<10} {'Time (s)':<10} {'Status'}")
    print("-" * 70)
    
    for result in results:
        status = "✅ Solved" if result['solved'] else "❌ Failed"
        steps = str(result['steps']) if result['solved'] else "N/A"
        print(f"{result['algorithm']:<25} {steps:<8} {result['nodes']:<10} {result['time']:<10.4f} {status}")
    
    # Find best performers
    solved_results = [r for r in results if r['solved']]
    if solved_results:
        best_steps = min(solved_results, key=lambda x: x['steps'])
        best_time = min(solved_results, key=lambda x: x['time'])
        best_efficiency = min(solved_results, key=lambda x: x['nodes'])
        
        print("\n🏆 BEST PERFORMERS:")
        print(f"  Optimal Path: {best_steps['algorithm']} ({best_steps['steps']} steps)")
        print(f"  Fastest Time: {best_time['algorithm']} ({best_time['time']:.4f}s)")
        print(f"  Most Efficient: {best_efficiency['algorithm']} ({best_efficiency['nodes']} nodes expanded)")
    
    # Ask user if they want to see step-by-step solutions
    print("\n" + "=" * 70)
    show_steps = input("Would you like to see step-by-step solutions? (y/n): ").lower().strip()
    
    if show_steps == 'y' or show_steps == 'yes':
        print("\nVisualization Options:")
        print("1. Compact view (side-by-side)")
        print("2. Detailed view (vertical)")
        viz_choice = input("Choose visualization type (1/2): ").strip()
        
        for name, solution_state in solution_states:
            if solution_state is not None:
                print(f"\n{'='*70}")
                choice = input(f"Show solution for {name}? (y/n/q to quit): ").lower().strip()
                if choice == 'q' or choice == 'quit':
                    break
                elif choice == 'y' or choice == 'yes':
                    if viz_choice == '1':
                        visualize_solution_compact(initial_state, solution_state, name)
                    else:
                        visualize_solution(initial_state, solution_state, name)

if __name__ == "__main__":
    print("🧩 Puzzle Game with 4 Search Algorithms 🧩")
    print("=" * 50)
    
    initial_state, goal_state = create_puzzle()
    run_all_algorithms(initial_state, goal_state) 