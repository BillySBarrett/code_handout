from typing import List, Tuple
import heapq
from Map import Map_Obj

# Create a map object with task=4
map_obj = Map_Obj(task=4)

def manhattan_eval(pos: List[int]) -> int:
    """
    Calculate the Manhattan distance between the given position and the end goal position.
    
    Args:
    - pos (List[int]): The current position as [y, x].
    
    Returns:
    - int: The Manhattan distance.
    """
    end_goal_pos = map_obj.get_end_goal_pos()
    return abs(end_goal_pos[0] - pos[0]) + abs(end_goal_pos[1] - pos[1])

def get_neighbors(pos: List[int]) -> List[List[int]]:
    """
    Get the neighboring cells of the given position.
    
    Args:
    - pos (List[int]): The current position as [y, x].
    
    Returns:
    - List[List[int]]: List of neighboring positions.
    """
    y, x = pos
    neighbors = [[y-1, x], [y+1, x], [y, x-1], [y, x+1]]
    return [n for n in neighbors if is_walkable(n)]

def is_walkable(pos: List[int]) -> bool:
    """
    Check if the given position is walkable (not a wall).
    
    Args:
    - pos (List[int]): The position to check.
    
    Returns:
    - bool: True if walkable, False otherwise.
    """
    value = map_obj.get_cell_value(pos)
    return value != -1  # Assuming -1 is the value for walls

def a_star(start: List[int], goal: List[int]) -> List[List[int]]:
    """
    Implement the A* search algorithm to find the shortest path from start to goal.
    
    Args:
    - start (List[int]): The starting position.
    - goal (List[int]): The goal position.
    
    Returns:
    - List[List[int]]: The path from start to goal.
    """
    start = tuple(start)
    goal = tuple(goal)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_eval(list(start))}

    while open_set:
        _, current = heapq.heappop(open_set)
        map_obj.set_cell_value(current, ' V ')

        if current == goal:
            return reconstruct_path(came_from, current)

        for neighbor in get_neighbors(list(current)):
            tentative_g_score = g_score[current] + map_obj.get_cell_value(neighbor)

            if tuple(neighbor) not in g_score or tentative_g_score < g_score[tuple(neighbor)]:
                came_from[tuple(neighbor)] = current
                g_score[tuple(neighbor)] = tentative_g_score
                f_score[tuple(neighbor)] = tentative_g_score + manhattan_eval(neighbor)
                heapq.heappush(open_set, (f_score[tuple(neighbor)], tuple(neighbor)))

    return []

def reconstruct_path(came_from: dict, current: Tuple[int, int]) -> List[List[int]]:
    """
    Reconstruct the path from start to goal using the came_from dictionary.
    
    Args:
    - came_from (dict): A dictionary mapping each position to its predecessor.
    - current (Tuple[int, int]): The current position.
    
    Returns:
    - List[List[int]]: The reconstructed path.
    """
    path = [list(current)]
    while current in came_from:
        current = came_from[current]
        path.append(list(current))
    path.reverse()
    return path

# Test
start = map_obj.get_start_pos()
goal = map_obj.get_goal_pos()
path = a_star(start, goal)
for pos in path:
    map_obj.set_cell_value(pos, ' P ')

# Print the length of the path
print(len(path))

# Display the map with the path
map_obj.show_map()

# Print the path
print(path)
