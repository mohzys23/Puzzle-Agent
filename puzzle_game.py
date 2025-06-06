import time
from algorithms import (
    PuzzleState,
    breadth_first_search,
    depth_first_search,
    a_star_search,
    greedy_best_first_search,
    get_solution_path
)

def get_solution_states(state):
    """Get all states in the solution path including initial state"""
    states = []
    current = state
    while current is not None:
        states.append(current)
        current = current.parent
    return states[::-1]

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
        for name, solution_state in solution_states:
            if solution_state is not None:
                print(f"\n{'='*70}")
                choice = input(f"Show solution for {name}? (y/n/q to quit): ").lower().strip()
                if choice == 'q' or choice == 'quit':
                    break
                elif choice == 'y' or choice == 'yes':
                    visualize_solution_compact(initial_state, solution_state, name)

if __name__ == "__main__":
    print("🧩 Puzzle Game with 4 Search Algorithms 🧩")
    print("=" * 50)
    
    initial_state, goal_state = create_puzzle()
    run_all_algorithms(initial_state, goal_state) 