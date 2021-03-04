# -------------------------------------------------------
### TileProblem class ###

# define a problem in terms of state, actions, transition functions, and goal test

# given an input file that contains the state, 
# your program should construct an instance of the problem as a TileProblem object

class TileProblem:
    def __init__(self, size, state):
        self.size = int(size)
        self.state = state
        self.actions = self.state_actions(self.state) # ['L', 'R', 'D', 'U']

    # transition functions (used to change state)

    # returns legal actions for the state
    def state_actions(self, state):
        state_actions = ['L', 'R', 'D', 'U']
        n = self.size
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

    # swap tiles, change state, return new problem
    def change_state(self, state, action):
        # TileProblem(size, state)
        copy = self.copy(state)
        problem = TileProblem(self.size, copy)
        n = self.size
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
        problem.state = copy
        return problem

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