import time
from algorithms import (
    breadth_first_search,
    depth_first_search,
    a_star_search,
    greedy_best_first_search
)
from utils import (
    create_puzzle,
    display_board,
    visualize_solution_compact,
    format_results_table,
    show_best_performers,
    create_result_entry
)

def run_all_algorithms(initial_state, goal_state):
    algorithms = [
        ("Breadth-First Search", breadth_first_search),
        ("Depth-First Search", depth_first_search),
        ("A* Search", a_star_search),
        ("Greedy Best-First Search", greedy_best_first_search)
    ]
    
    print(f"\n Running Difficult Puzzle - Ultimate Challenge!")
    print("=" * 60)
    print("Initial State:")
    display_board(initial_state.board)
    print("Goal State:")
    display_board(goal_state.board)
    print("=" * 60)
    
    results = []
    solution_states = []
    
    # Use higher depth limit for this challenging puzzle
    dfs_depth = 60
    
    for name, algorithm in algorithms:
        print(f"\n{name}:")
        start_time = time.time()
        
        if name == "Depth-First Search":
            result = algorithm(initial_state, goal_state, max_depth=dfs_depth)
        else:
            result = algorithm(initial_state, goal_state)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        path, nodes_expanded, path_length, solution_state = result
        
        if path is not None:
            print(f"✅ Solution found!")
            print(f"Moves: {' -> '.join(path) if path else 'Already solved'}")
            print(f"Path length: {path_length}")
            print(f"Nodes expanded: {nodes_expanded:,}")
            print(f"Time taken: {execution_time:.4f} seconds")
        else:
            print(f"❌ No solution found within limits")
            print(f"Nodes expanded: {nodes_expanded:,}")
            print(f"Time taken: {execution_time:.4f} seconds")
        
        # Create result entry using utility function
        result_entry, solution_state_entry = create_result_entry(
            name, path, nodes_expanded, execution_time, solution_state
        )
        results.append(result_entry)
        solution_states.append((name, solution_state_entry))
    
    # Use utility functions for formatting
    format_results_table(results)
    show_best_performers(results)
    
    # Show challenge analysis
    print(f"\n🎯 CHALLENGE ANALYSIS:")
    solved_count = sum(1 for r in results if r['solved'])
    print(f"  Algorithms that conquered the challenge: {solved_count}/4")
    if solved_count > 0:
        avg_nodes = sum(r['nodes'] for r in results if r['solved']) / solved_count
        print(f"  Average nodes explored: {avg_nodes:,.0f}")
        print(f"  This is one of the most challenging 8-puzzle configurations!")
    
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
    print("Puzzle Challenge - Ultimate 8-Puzzle Test! 🧩")
    print("=" * 60)
    print("Prepare for the most challenging 8-puzzle configuration!")
    print("   This puzzle will test the limits of each search algorithm.")
    
    initial_state, goal_state = create_puzzle()
    run_all_algorithms(initial_state, goal_state) 