import sys
from dataclasses import dataclass, field
from typing import Any
import queue
from TileProblem import TileProblem
from Heuristics import Heuristics

# -------------------------------------------------------

def input_to_state(n, file):
    n = int(n)
    state = [[0]*n for _ in range(n)]
    index = 0
    f = open(file)
    for line in f:
        line = line.strip('\n')
        numbers = line.split(",")
        state[index] = numbers
        index += 1
    return state

def write_output(path, file):
    output = ",".join(path)
    f = open(file, "w")
    for ch in output:
        f.write(ch)
    f.close()
    return True

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)

class Node:
    def __init__(self, problem, parent=None, action=None):
        self.problem = problem
        self.parent = parent
        self.action = action
        self.state = problem.state
        # g(n)
        if (self.parent != None):
            # cost of parent's path + distance from between parent and node
            self.g = parent.g + 1 
        else:
            self.g = 0
        # f(n) = g(n) + h(n)

def reconstruct_path(node):
    solution = []
    ptr = node
    while(ptr.parent!=None):
        solution.insert(0, ptr.action)
        ptr = ptr.parent
    return solution

def a_star(problem, h):
    # frontier = priority_queue() # sort frontier on expected path cost
    frontier = queue.PriorityQueue()
    # frontier = frontier + make-node(start)
    start = Node(problem)
    frontier.put(PrioritizedItem(0, start))
    explored = []

    # f(n) = g(n) + h(n)
    # g(n) = cost of path from start to n so far (dist from root)
    # h(n) = estimated cost from n to G (end node)

    # start has no parent
    # start.g = 0
    start.h = h(start.state)
    start.f = start.g + start.h

    # while not frontier.isempty():
    while not frontier.empty():
        # current <- pop(frontier) # i.e., the top of the queue
        current = frontier.get().item
        # if goal-test(current) return success # goal test when node expands
        if problem.goal_test(current.state):
            return reconstruct_path(current) 
        # if current not in explored:
        if not current in explored:
            # explored <- explored + current.state
            explored.append(current.state)
            # for each action in current.actions():
            for action in problem.state_actions(current.state): # neighbors/sucessors
                # new <- action(current.state)
                new = problem.change_state(current.state, action) # new problem
                # new-node <- make-node(new, current, action)
                new_node = Node(new, current, action) # neighbor
                # new_node.g = new_node.parent.g + 1 
                new_node.h = h(new_node.state)
                new_node.f = new_node.g + new_node.h
                
                if (not new_node.state in explored):
                    # frontier = frontier + new-node
                    frontier.put(PrioritizedItem(new_node.f, new_node))
    return False

# -------------------------------------------------------
### Main class ###

if __name__ == '__main__':
    # python puzzleSolver.py <A> <N> <H> <INPUT FILE PATH> <OUTPUT FILE PATH>
    # A is the algorithm (A=1 for A* and A=2 for RBFS)
    # N is the size of the puzzle (N=3 for 8-puzzle and N=4 for 15-puzzle)
    # H is for heuristics (H=1 for h1 and H=2 for h2)

    # (sys.argv[0]) # puzzleSolver.py
    a = (sys.argv[1]) # A
    n = (sys.argv[2]) # N
    h = (sys.argv[3]) # H
    input = (sys.argv[4]) # INPUT FILE PATH
    output = (sys.argv[5]) # OUTPUT FILE PATH

    problem = TileProblem(n, input_to_state(n, input)) # TileProblem(size, state)
    heuristics = Heuristics()
    solution = []

    print(problem.state)

    if (a == '1'):
        if (h == '1'):
            solution = a_star(problem, heuristics.manhattan_distance)
        elif (h == '2'):
            solution = a_star(problem, heuristics.hamming_distance)
    elif (a == '2'):
        print("rbfs")
    
    write_output(solution, output)

    # arr1 = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '']]
    # arr2 = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15','']]
    # arr3 = [['1', '2', '4'], ['3', '5', '6'], ['8', '7', '']]
    # arr4 = [['1', '3', '2'], ['', '5', '6'], ['8', '7', '4']]
    
    # state = problem.state
    # print(problem.goal_test(state))
    # print(problem.state_actions(state))
    # print(problem.change_state(state, 'U').state)

    # print(a_star(problem, heuristics.hamming_distance))
    # print(a_star(problem, heuristics.manhattan_distance))

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