"""
COMS W4701 Artificial Intelligence - Homework 2 Programming

In this assignment you will implement and compare different
search strategies for solving the n-Puzzle, which is a generalization
of the 8 puzzle to squares of arbitrary size.

@author: Roxanne Farhad raf2192
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped. 
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]
    
    new_state = []
    for row in range(len(state)): 
        new_row = []
        for column in range(len(state[row])): 
            if row == i1 and column == j1: 
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else: 
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions. 
    The result should be a list containing (Action, state) tuples. 
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))), 
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))] 
    """
    child_states = []

    for row in range(len(state)):
        for column in range(len(state[row])):
            if state[row][column] == 0:
                if column < len(state)-1: # Left
                    new_state = swap_cells(state, row,column, row, column+1)
                    child_states.append(("Left",new_state))
                if column > 0: # Right
                    new_state = swap_cells(state, row,column, row, column-1)
                    child_states.append(("Right",new_state))
                if row < len(state)-1:   #Up
                    new_state = swap_cells(state, row,column, row+1, column)
                    child_states.append(("Up",new_state))
                if row > 0: # Down
                    new_state = swap_cells(state, row,column, row-1, column)
                    child_states.append(("Down", new_state))
                break
    return child_states

            
def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise. 
    """    
    counter = 0
    for row in state:
        for cell in row:
            if counter != cell:
                return False
            counter += 1
    return True

def dfs(state):
    """
    Breadth first search.
    Returns four values: A path (list of actions), path cost, the number of states expanded,
    and the maximum size of the frontier.
    You should also have two mutable data structures:
    - The frontier of nodes to expand (operating as a queue in BFS)
    - A set of nodes already expanded
    """
    states_expanded = 0
    max_frontier = 0

    frontier = []
    explored = set()
    path = []
    path_cost = 0
    frontier_set = set() # set of all elements in the frontier 
    
    frontier.append(state)
    frontier_set.add(state)
    parent = {}
    parent[state] = ("root", "none") #the root value has no parent
    
    while(len(frontier)):
        leaf = frontier.pop()
        frontier_set.remove(leaf); 
        explored.add(leaf)

        if(goal_test(leaf)):
            while(parent.get(leaf) != ("root", "none")):
                value = parent.get(leaf)
                action = value[1]
                path.insert(0, action)
                leaf = value[0]
                path_cost+=1;
            
            return path, path_cost, states_expanded, max_frontier
        
        states_expanded += 1
        
        for i in get_successors(leaf):
            if(i[1] not in explored and i[1] not in frontier_set):
                frontier.append(i[1])
                frontier_set.add(i[1])
                parent[i[1]] = (leaf, i[0])
        if(len(frontier) > max_frontier):
            max_frontier = len(frontier)

    #  return path, path cost, num states expanded, max size of frontier
    return path, 0, states_expanded, max_frontier # No solution found - Python automatically constructs a tuple to return values.
                               
     
def bfs(state):
    """
    Depth first search.
    Returns four values: A path (list of actions), path cost, the number of states expanded,
    and the maximum size of the frontier.
    You should also have two mutable data structures:
    - The frontier of nodes to expand (operating as a queue in BFS)
    - A set of nodes already expanded
    """
    states_expanded = 0
    max_frontier = 0

    frontier = []
    explored = set()
    path = []
    path_cost = 0
    max_frontier = 0;
    frontier_set = set();
    
    frontier.append(state)
    frontier_set.add(state); 
    parent = {}
    parent[state] = ("root", "none") #the root value has no parent
    
    while(len(frontier)):
        leaf = frontier.pop()
        explored.add(leaf)
        frontier_set.remove(leaf); 

        if(goal_test(leaf)):
            while(parent.get(leaf) != ("root", "none")):
                value = parent.get(leaf)
                action = value[1]
                path.insert(0, action)
                leaf = value[0]
                path_cost+=1;
            return path, path_cost, states_expanded, max_frontier

        states_expanded += 1

        for i in get_successors(leaf):
            if((i[1] not in explored) and i[1] not in frontier_set):
                frontier.insert(0, i[1])
                frontier_set.add(i[1])
                parent[i[1]] = (leaf, i[0])
        if(len(frontier) > max_frontier):
            max_frontier = len(frontier)

    #  return path, path cost, num states expanded, max size of frontier
    return None, 0, states_expanded, max_frontier # No solution found

def misplaced_heuristic(state):

    counter = 0
    value = 0
    for row in state:
        for cell in row:
            if counter != cell and cell != 0:
                value += 1
            counter += 1
    
    return value

def mhs(val, state):
    
    rows  = len(state) # number of rows
    columns = len(state[0]) # number of columns
    
    targetX = int(val/rows)
    targetY = val%columns

    for i in range(rows): # this refers to the row
        for j in range(columns): # this refers to the col
            if(val == state[i][j]):
                return (abs(i - targetX) + abs(j - targetY))
            

def manhattan_heuristic(state):
    """
        For each misplaced tile, compute the Manhattan distance between the current
        position and the goal position. Then return the sum of all distances.
    """
    misplaced = 0;
    value = 0
    
    for row in state:
        for cell in row:
            if value != cell and cell != 0:
                mhs1 = mhs(cell, state)
                misplaced = misplaced + mhs1
            value+=1

    return misplaced



def astar(state, heuristic):
    """
    A-star search.
    Returns four values: A path (list of actions), path cost, the number of states expanded,
    and the maximum size of the frontier.
    You should also have two mutable data structures:
    - The frontier of nodes to expand (operating as a queue in BFS)
    - A set of nodes already expanded
    """
    # Use these modules to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_frontier = 0

    frontier = []
    explored = set()
    path = []
    path_cost = 0
    max_frontier = 0;
    frontier_set = set()
    
    parent = {}
    parent[state] = ("root", "none", 0) #the root value has no parent

    heappush(frontier, (0 + heuristic(state), state)) # adds the state to the pq
    #  return path, path cost, num states expanded, max size of frontier
    frontier_set.add(state); 

    while(len(frontier)):
        leaf = heappop(frontier)[1]
        frontier_set.remove(leaf)
        explored.add(leaf)
        if(goal_test(leaf)):
            while(parent.get(leaf) != ("root", "none", 0)):
                value = parent.get(leaf)
                action = value[1]
                path.insert(0, action)
                leaf = value[0]
                path_cost+=1
            
            return path, path_cost, states_expanded, max_frontier
        states_expanded += 1

        for i in get_successors(leaf):
            if(i[1] not in explored and i[1] not in frontier_set):
                hCost = heuristic(i[1])
                backward_cost = parent.get(leaf)[2]
                total_cost = hCost + backward_cost
                heappush(frontier, (total_cost, i[1]))
                frontier_set.add(i[1])
                parent[i[1]] = (leaf, i[0], backward_cost + 1)
        
        if(len(frontier) > max_frontier):
                max_frontier = len(frontier)
               
    
    return None, 0, states_expanded, max_frontier # No solution found

def print_result(path_cost, states_expanded, max_frontier):
    """
    Helper function to format test output.
    """
    print("Cost of path: {}".format(path_cost))
    print("States expanded: {}".format(states_expanded))
    print("Max frontier size: {}".format(max_frontier))



if __name__ == "__main__":

    #Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8), 
                  (3, 6, 7))  

    #More difficult test case
    #test_state = ((7, 2, 4),
    #             (5, 0, 6),
    #             (8, 3, 1))


    print(state_to_string(test_state))
    print()

    print("====BFS====")
    start = time.time()
    path, path_cost, states_expanded, max_frontier = bfs(test_state)
    end = time.time()
    print("Path to goal: {}".format(path))
    print_result(path_cost, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====DFS====")
    start = time.time()
    path, path_cost, states_expanded, max_frontier = dfs(test_state)
    end = time.time()
    print_result(path_cost, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    
    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    path, path_cost, states_expanded, max_frontier = astar(test_state, misplaced_heuristic)
    end = time.time()
    print("Path to goal: {}".format(path))
    print_result(path_cost, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    path, path_cost, states_expanded, max_frontier = astar(test_state, manhattan_heuristic)
    end = time.time()
    print("Path to goal: {}".format(path))
    print_result(path_cost, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

