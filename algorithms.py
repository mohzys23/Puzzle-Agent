import heapq
from collections import deque
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
        
        moves = [(-1, 0, 'UP'), (1, 0, 'DOWN'), (0, -1, 'LEFT'), (0, 1, 'RIGHT')]
        
        for dr, dc, move_name in moves:
            new_row, new_col = blank_row + dr, blank_col + dc
            
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_board = copy.deepcopy(self.board)
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
                    for gi in range(self.size):
                        for gj in range(self.size):
                            if goal_state.board[gi][gj] == value:
                                distance += abs(i - gi) + abs(j - gj)
                                break
        return distance

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
    
    return None, nodes_expanded, 0, None

def depth_first_search(initial_state, goal_state, max_depth=50):
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
    
    return None, nodes_expanded, 0, None

def a_star_search(initial_state, goal_state):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    open_list = []
    heapq.heappush(open_list, (0, 0, initial_state))
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
    
    return None, nodes_expanded, 0, None

def greedy_best_first_search(initial_state, goal_state):
    if initial_state == goal_state:
        return [], 1, 0, initial_state
    
    open_list = []
    heapq.heappush(open_list, (0, initial_state))
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
    
    return None, nodes_expanded, 0, None 