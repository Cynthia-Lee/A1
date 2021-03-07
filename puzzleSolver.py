import sys
from dataclasses import dataclass, field
from typing import Any
import queue
from TileProblem import TileProblem
from Heuristics import Heuristics
import datetime

# -------------------------------------------------------
# Sources used:
# Lecture slides
# https://pages.mtu.edu/~nilufer/classes/cs5811/2012-fall/lecture-slides/cs5811-ch03-search-b-informed-v2.pdf
# http://mas.cs.umass.edu/classes/cs683/lectures-2010/Lec5_Search4-F2010-4up.pdf
# https://en.wikipedia.org/wiki/Admissible_heuristic
# -------------------------------------------------------

# takes in input file and returns a 2d array to represent the state
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

# writes the solution path array to the output file
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
    # print("Depth", len(solution))
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
            # print("Number of states explored:", len(explored)+1, "ANSWER:", reconstruct_path(current))
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

counter = 1

def recursive_best_first_search(problem, h):
    global counter
    counter = 1
    # solution, fvalue <- rbfs(problem, node(problem.initial), inf, h)
    start = Node(problem)
    start.h = h(start.state)
    start.f = start.g + start.h
    solution = rbfs(problem, start, float("inf"), h)
    return solution

def rbfs(problem, node, f_limit, h):
    # returns solution or failure, and a new f-cost limit
    if (problem.goal_test(node.state)):
        return reconstruct_path(node)
    sucessors = []
    for action in problem.state_actions(node.state, node.action): # neighbors/sucessors
        # add child_node(problem, node, action) into sucessors
        new = problem.change_state(node.state, action) # new problem
        child_node = Node(new, node, action) # neighbor
        child_node.h = h(child_node.state)
        child_node.f = child_node.g + child_node.h
        sucessors.append(child_node)
    if (not sucessors): # if successors is empty
        # return failure, infinity
        return (False, float("inf"))
    for s in sucessors:
        # update f with value from previous search if any
        s.f = max(s.g + s.h, node.f)
    # loop do
    while True:
        # best <- lowest f-value in successors
        best = sucessors[0]
        alternative = best
        for s in sucessors:
            if (s.f <= best.f):
                alternative = best
                best = s
            elif (s.f <= alternative.f):
                alternative = s
        # if best.f > f-limit then return failure, best.f
        if (best.f > f_limit):
            return (False, best.f)
        # alternative <- the second lowest f-value among successors
        # result, best.f <- RBFS(problem, best, min(f-limit,alternative))
        global counter
        counter += 1
        result = rbfs(problem, best, min(f_limit, alternative.f), h)
        best.f = result[1]
        # if result not = failure then return result
        if (result[0]):
            return result

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

    # print(problem.state)
    start = datetime.datetime.now()
    
    if (a == '1'):
        if (h == '1'):
            solution = a_star(problem, heuristics.manhattan_distance)
        elif (h == '2'):
            solution = a_star(problem, heuristics.hamming_distance)
    elif (a == '2'):
        if (h == '1'):
            solution = recursive_best_first_search(problem, heuristics.manhattan_distance)
        elif (h == '2'):
            solution = recursive_best_first_search(problem, heuristics.hamming_distance)
    
    write_output(solution, output)

    end = datetime.datetime.now()
    # hour, minute, second
    print((end - start) * 1000.0) 
    
    '''
    # TESTS
    heuristics = Heuristics()
    problem1 = TileProblem(3, input_to_state(3, "puzzle1.txt"))
    problem2 = TileProblem(3, input_to_state(3, "puzzle2.txt"))
    problem3 = TileProblem(3, input_to_state(3, "puzzle3.txt"))
    problem4 = TileProblem(4, input_to_state(4, "puzzle4.txt"))
    problem5 = TileProblem(4, input_to_state(4, "puzzle5.txt"))
    # A* with hamming
    print("A* with hamming")
    print(a_star(problem1, heuristics.hamming_distance))
    print(a_star(problem2, heuristics.hamming_distance))
    print(a_star(problem3, heuristics.hamming_distance))
    print(a_star(problem4, heuristics.hamming_distance))
    print(a_star(problem5, heuristics.hamming_distance))
    # A* with manhattan
    print("A* with manhattan")
    print(a_star(problem1, heuristics.manhattan_distance))
    print(a_star(problem2, heuristics.manhattan_distance))
    print(a_star(problem3, heuristics.manhattan_distance))
    print(a_star(problem4, heuristics.manhattan_distance))
    print(a_star(problem5, heuristics.manhattan_distance))
    # RBFS with hamming
    print("RBFS with hamming")
    print(recursive_best_first_search(problem1, heuristics.hamming_distance), counter)
    print(recursive_best_first_search(problem2, heuristics.hamming_distance), counter)    
    print(recursive_best_first_search(problem3, heuristics.hamming_distance), counter) 
    print(recursive_best_first_search(problem4, heuristics.hamming_distance), counter)
    print(recursive_best_first_search(problem5, heuristics.hamming_distance), counter)
    # RBFS with manhattan
    print("RBFS with manhattan")
    print(recursive_best_first_search(problem1, heuristics.manhattan_distance), counter)
    print(recursive_best_first_search(problem2, heuristics.manhattan_distance), counter)
    print(recursive_best_first_search(problem3, heuristics.manhattan_distance), counter)
    print(recursive_best_first_search(problem4, heuristics.manhattan_distance), counter)
    print(recursive_best_first_search(problem5, heuristics.manhattan_distance), counter)
    '''

    # if any of your moves is illegal (e.g., moves the blank space out-of-bounds)
    # then the output is considered a failure