import math

# -------------------------------------------------------
### Heuristics class ###

# two different admissible (or consistent) heuristic functions (h1 and h2)
# one should dominate the other: heuristic h1 dominates h2 if h1(n) > h2(n) for all n

# Heuristics class that defines methods 
# that compute the heuristics for calculating distance to the goal

# h1(n) = total Manhattan distance
# h2(n) = number of misplaced tiles (Hamming distance)

# h1(n) dominates h2(n)
# if h1(n) >= h2(n) for all n (both admissible)
# h1 dominates h2 and is better for search

class Heuristics:
    #def __init__(self):
    #    self.data = []

    def hamming_distance(self, state):
        n = len(state[0])
        value = 0
        if(state[n-1][n-1] != ''):
            value += 1
        row = 0
        col = 0
        for check in range(n*n-1):
            if (state[row][col] != str(check+1)):
                value += 1
            col += 1
            if (col == n):
                row +=1 
                col = 0 
        return value

    def manhattan_distance(self, state):
        n = len(state[0])
        value = 0
        row = 0
        col = 0
        for check in range(n*n):
            # number check
            num_check = state[row][col] != '' and state[row][col] != str(check+1)
            # '' check
            e_check = (state[row][col] == '' and (row != n-1 or col != n-1))
            if (num_check or e_check):
                # print(row, col, "=", state[row][col])
                if (state[row][col] == ''):
                    tile_value = (n-1)-row + (n-1)-col
                else:
                    num = int(state[row][col])
                    # print(row, col)
                    # print(num, "correct row", math.floor((num-1)/n))
                    # print(num, "correct col", (num-1)%n)
                    # print("move", abs(math.floor((num-1)/n) - row))
                    # print("move", abs((num-1)%n - col))
                    tile_value = abs(math.floor((num-1)/n) - row) + abs((num-1)%n - col)
                value += tile_value
            col += 1
            if (col == n):
                row +=1 
                col = 0 
        return value
