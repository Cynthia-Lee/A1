import sys
import queue
from TileProblem import TileProblem
from Heuristics import Heuristics

# python puzzleSolver.py <A> <N> <H> <INPUT FILE PATH> <OUTPUT FILE PATH>
# A is the algorithm (A=1 for A* and A=2 for RBFS)
# N is the size of the puzzle (N=3 for 8-puzzle and N=4 for 15-puzzle)
# H is for heuristics (H=1 for h1 and H=2 for h2)

# (sys.argv[0]) # puzzleSolver.py
A = (sys.argv[1]) # A
N = (sys.argv[2]) # N
H = (sys.argv[3]) # H
INPUT = (sys.argv[4]) # INPUT FILE PATH
OUTPUT = (sys.argv[5]) # OUTPUT FILE PATH

class Node:
    def __init__(self, problem, parent=None, action=None):
        self.problem = problem
        self.parent = parent
        self.action = action
        self.state = problem.initial_state
        # f(n)
        # g(n)
        # h(n)
        self.priority = 0

def a_star(problem, h):
    # frontier = priority_queue() # sort frontier on expected path cost
    frontier = queue.PriorityQueue()
    # frontier = frontier + make-node(start)
    start = Node(problem)
    frontier.put(0, start)
    explored = []

    # f(n) = g(n) + h(n)
    # g(n) = cost of path from start to n so far (dist from root)
    # h(n) = estimated cost from n to G (end node)
    start.g = 0
    start.h = h(start.state)
    start.f = start.g + start.h

    # while not frontier.isempty():
    while not frontier.empty():
        # current <- pop(frontier) # i.e., the top of the queue
        current = frontier.get()
        # if goal-test(current) return success # goal test when node expands
        if problem.goal_test(current.state):
            return True 

        

        # if current not in explored:
        if not current in explored:
            # explored <- explored + current.state
            explored.append(current)
            # for each action in current.actions():
            for action in problem.state_actions(current.state):
                # new <- action(current.state)
                new = problem.change_state(current.state, action)
                # new-node <- make-node(new, current, action)
                new_node = Node(new, current, action)
                # frontier = frontier + new-node
                frontier.append(new_node)
                
    return False

# -------------------------------------------------------
### Main class ###

if __name__ == '__main__':
    problem = TileProblem(A, N, H, INPUT, OUTPUT)
    heuristics = Heuristics()

    print(problem.initial_state)
    arr1 = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '']]
    arr2 = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15','']]
    arr3 = [['1', '2', '4'], ['3', '5', '6'], ['8', '7', '']]
    arr4 = [['1', '3', '2'], ['', '5', '6'], ['8', '7', '4']]
    
    state = problem.initial_state
    print(problem.goal_test(state))
    print(problem.state_actions(state))
    print(problem.change_state(state, 'U'))
    print(state)

    

    # print(heuristics.hamming_distance(state))
    # print(heuristics.manhattan_distance(state))

    # print(arr3)
    # print(heuristics.manhattan_distance(arr3))

    # print(heuristics.manhattan_distance(arr4))

    # print("GOOD")
    # print(problem.goal_test(arr1))
    # print(problem.goal_test(arr2))
    # print("BAD")
    # print(problem.goal_test(arr3))

    # if any of your moves is illegal (e.g., moves the blank space out-of-bounds)
    # then the output is considered a failure