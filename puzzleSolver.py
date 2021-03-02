import sys
from dataclasses import dataclass, field
from typing import Any
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
            explored.append(current)
            # for each action in current.actions():
            for action in problem.state_actions(current.state): # neighbors
                # new <- action(current.state)
                new = problem.change_state(current.state, action)  # new problem
                # new-node <- make-node(new, current, action)
                new_node = Node(new, current, action) # neighbor

                # tentative_g = current.g + distance between current and successor
                tentative_g = current.g + 1 
                if (tentative_g < new_node.g):
                    # this path is better than any previous one
                    new_node.parent = current
                    new_node.g = tentative_g
                    print("test")

                # new_node.g = new_node.parent.g + 1 
                new_node.h = h(new_node.state)
                new_node.f = new_node.g + new_node.h
                # frontier = frontier + new-node
                frontier.put(PrioritizedItem(new_node.f, new_node))
    return False

# -------------------------------------------------------
### Main class ###

if __name__ == '__main__':
    problem = TileProblem(A, N, H, INPUT, OUTPUT)
    heuristics = Heuristics()

    print(problem.state)
    arr1 = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '']]
    arr2 = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15','']]
    arr3 = [['1', '2', '4'], ['3', '5', '6'], ['8', '7', '']]
    arr4 = [['1', '3', '2'], ['', '5', '6'], ['8', '7', '4']]
    
    # state = problem.state
    # print(problem.goal_test(state))
    # print(problem.state_actions(state))
    # print(problem.change_state(state, 'U').state)

    print(a_star(problem, heuristics.hamming_distance))
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