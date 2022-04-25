from utils import *
from search import *

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________
  

# ______________________________________________________________________________

class Sudoku(Problem):
    def __init__(self, initial,  N = 9):
        self.N = N
        super().__init__(initial, goal = None)
    
    def find_blank(self, state):
        for row in range(self.N):
            for col in range(self.N):
                if(state[row * self.N + col] == 0):
                    return row, col
        return -1, -1

    def is_valid_row(self, state, row, value):
        for i in range(self.N):
            if(state[self.N * row + i] == value):
                return False
        return True

    def is_valid_col(self, state, col, value):
        for i in range(self.N):
            if(state[self.N * i + col] == value):
                return False
        return True

    def is_valid_box(self, state, row, col, value):
        square_row_start = (row // 3) * 3
        square_col_start = (col // 3) * 3

        for row in range(square_row_start, square_row_start + 3):
            for col in range(square_col_start, square_col_start + 3):
                if state[row * self.N +  col] == value:
                    return False
        return True

    def actions(self, state):
        possible_actions = []

        row, col = self.find_blank(state)
        if(row == -1 and col == -1):
            return []

        values = random.sample(range(1, 10), 9)
        r = random.randint(0, 100)
        for value in values:
            # approach 1
            if r < 15:
                if self.is_valid_row(state, row, value) and self.is_valid_col(state, col, value):
                    possible_actions.append((row, col, value))
            elif r < 30:
                if self.is_valid_row(state, row, value) and self.is_valid_box(state, row, col, value):
                    possible_actions.append((row, col, value))
            else:
                if self.is_valid_row(state, row, value) and self.is_valid_col(state, col, value) and self.is_valid_box(state, row, col, value):
                    possible_actions.append((row, col, value))

            # approach 2
            # count = state.count(value)
            # if(count < 9):
            #     possible_actions.append((row, col, value))

        return possible_actions 
    
    def result(self, state, action):
        new_state = list(state)
        new_state[action[0] * self.N + action[1]] = action[2]
        return tuple(new_state) 
        
    def get_row(self, row_index, x):

        return x[9*row_index: 9*(row_index+1)]

    def get_col(self, col_index, x):
        return [x[9*row + col_index] for row in range(9)]

    def get_box(self, box_index, x):
        row_start = (box_index // 3) * 3
        col_start = (box_index % 3) * 3
        box = []

        for row in range(row_start, row_start + 3):
            for col in range(col_start, col_start + 3):
                box.append(x[row*9 + col])
        return box 

    def goal_test(self, state):
        for row in range(self.N):
            for col in range(self.N):
                if(state[row * self.N + col] == 0):
                    return False        

        for i in range(self.N):
            row_i = self.get_row(i, state)
            if(is_duplicate(row_i)):
                return False

            col_i = self.get_col(i, state)
            if(is_duplicate(col_i)):
                return False

            box_i = self.get_box(i, state)
            if(is_duplicate(box_i)):
                return False
        return True
    
    def printScoreHeuristic(self, node):
        score = 0
        if node.action:
            row, col, value = node.action

            row_i = self.get_row(row, node.state)
            col_i = self.get_col(col, node.state)
            box_i = self.get_box((row*9 + col) // 9, node.state)
            
            score = num_duplicate(row_i) + num_duplicate(col_i) + num_duplicate(box_i)
            print(f'Score : {num_duplicate(row_i)} + {num_duplicate(col_i)} + {num_duplicate(box_i)}, Depth: {node.depth}')

    def h(self, node):
        score = 0
        if node.action:
            row, col, value = node.action

            row_i = self.get_row(row, node.state)
            col_i = self.get_col(col, node.state)
            start_row = row // 3
            start_col = col // 3
            box_i = self.get_box((start_row*3 + start_col), node.state)
            
            score = (num_duplicate(row_i) + num_duplicate(col_i) + num_duplicate(box_i) + 1) *  node.state.count(0)
            
        return score

