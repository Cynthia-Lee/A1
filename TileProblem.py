# -------------------------------------------------------
### TileProblem class ###

# define a problem in terms of state, actions, transition functions, and goal test

# given an input file that contains the state, 
# your program should construct an instance of the problem as a TileProblem object

class TileProblem:
    def __init__(self, algorithm, size, heuristic, input_file, output_file):
        self.algorithm = algorithm
        self.size = size
        self.heuristic = heuristic
        self.input_file = input_file
        self.output_file = output_file
        self.initial_state = self.input_to_state()
        self.actions = self.state_actions(self.initial_state) # ['L', 'R', 'D', 'U']

    def input_to_state(self):
        n = int(self.size)
        state = [[0]*n for _ in range(n)]
        index = 0
        f = open(self.input_file)
        for line in f:
            line = line.strip('\n')
            numbers = line.split(",")
            state[index] = numbers
            index += 1
        return state

    # transition functions (used to change state)
    def state_actions(self, state):
        # return legal actions
        state_actions = ['L', 'R', 'D', 'U']
        n = int(self.size)
        row = 0
        col = 0
        for check in range(n*n-1):
            if (state[row][col] == ''):
                break
            col += 1
            if (col == n):
                row +=1 
                col = 0  
        # check left
        if (col == 0):
            state_actions.remove('L')
        # check right
        if (col == n-1):
            state_actions.remove('R')
        # check down
        if (row == n-1):
            state_actions.remove('D')
        # check up
        if (row == 0):
            state_actions.remove('U')
        return state_actions

    def copy(self, state):
        newState = []
        for row in state:
            newState.append([item for item in row])
        return newState

    # swap tiles, update state
    def change_state(self, state, action):
        copy = self.copy(state)
        n = int(self.size)
        r = 0
        c = 0
        for check in range(n*n-1):
            if (copy[r][c] == ''):
                break
            c += 1
            if (c == n):
                r +=1 
                c = 0  
        if (action == 'L'):
            # col - 1
            copy[r][c], copy[r][c-1] = copy[r][c-1], copy[r][c]
        elif (action == 'R'):
            # col + 1
            copy[r][c], copy[r][c+1] = copy[r][c+1], copy[r][c]
        elif (action == 'D'):
            # row + 1
            copy[r][c], copy[r+1][c] = copy[r+1][c], copy[r][c]
        elif (action == 'U'):
            # row - 1
            copy[r][c], copy[r-1][c] = copy[r-1][c], copy[r][c]
        return copy

    def goal_test(self, state): 
        n = len(state[0])
        if(state[n-1][n-1] != ''):
            return False
        row = 0
        col = 0
        for check in range(n*n-1):
            # print(state[math.floor(check/n)][check%n] == str(check+1))
            # if ((state[math.floor(check/n)][check%n] != str(check+1))):
                # return False
            # print(row, col, " = ", check+1)
            if (state[row][col] != str(check+1)):
                return False
            col += 1
            if (col == n):
                row +=1 
                col = 0
        return True