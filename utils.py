from algorithms import PuzzleState, get_solution_path

def create_puzzle():
    """Create the ultimate 8-puzzle challenge - Nightmare difficulty"""
    # This configuration is designed to be one of the hardest possible
    # requiring extensive search to solve
    initial_board = [
        [8, 7, 6],
        [0, 4, 1],
        [2, 5, 3]
    ]
    
    goal_board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    return PuzzleState(initial_board), PuzzleState(goal_board)



def get_solution_states(state):
    """Get all states in the solution path including initial state"""
    states = []
    current = state
    while current is not None:
        states.append(current)
        current = current.parent
    return states[::-1]

def display_board(board):
    """Display a puzzle board in a readable format"""
    for row in board:
        print([x if x != 0 else ' ' for x in row])
    print()

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

def format_results_table(results):
    """Format and display results in a clean table"""
    print("\n" + "=" * 70)
    print("📊 ALGORITHM PERFORMANCE SUMMARY")
    print("=" * 70)
    print(f"{'Algorithm':<25} {'Steps':<8} {'Nodes':<10} {'Time (s)':<10} {'Status'}")
    print("-" * 70)
    
    for result in results:
        status = "✅ Solved" if result['solved'] else "❌ Failed"
        steps = str(result['steps']) if result['solved'] else "N/A"
        print(f"{result['algorithm']:<25} {steps:<8} {result['nodes']:<10} {result['time']:<10.4f} {status}")

def show_best_performers(results):
    """Display best performing algorithms"""
    solved_results = [r for r in results if r['solved']]
    if solved_results:
        best_steps = min(solved_results, key=lambda x: x['steps'])
        best_time = min(solved_results, key=lambda x: x['time'])
        best_efficiency = min(solved_results, key=lambda x: x['nodes'])
        
        print("\n🏆 BEST PERFORMERS:")
        print(f"  Optimal Path: {best_steps['algorithm']} ({best_steps['steps']} steps)")
        print(f"  Fastest Time: {best_time['algorithm']} ({best_time['time']:.4f}s)")
        print(f"  Most Efficient: {best_efficiency['algorithm']} ({best_efficiency['nodes']} nodes expanded)")

def create_result_entry(name, path, nodes_expanded, execution_time, solution_state):
    """Create a standardized result entry"""
    if path is not None:
        return {
            'algorithm': name,
            'solved': True,
            'steps': len(path),
            'nodes': nodes_expanded,
            'time': execution_time,
            'moves': ' -> '.join(path) if path else 'Already solved'
        }, solution_state
    else:
        return {
            'algorithm': name,
            'solved': False,
            'steps': 0,
            'nodes': nodes_expanded,
            'time': execution_time,
            'moves': 'No solution'
        }, None 