from collections import deque
from sudoku import *
from utils import *

def depth_first_graph_search(problem):
    """
    [Figure 3.7]
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Does not get trapped by loops.
    If two paths reach a state, only use the first one.
    """
    frontier = [(Node(problem.initial))]  # Stack

    explored = set()
    i = 0
    count = 1 
    while frontier:
        print(f'Step: {i}, Count: {count}')
        node = frontier.pop()
        print(f"Action: {node.action}")
        print(repr(node))
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        temp = len(frontier)
        frontier.extend(child for child in node.expand(problem) if child.state not in explored and child not in frontier)
        count += len(frontier) - temp
        i += 1
    return None

def breadth_first_graph_search(problem):
    """[Figure 3.11]
    Note that this function can be implemented in a
    single line as below:
    return graph_search(problem, FIFOQueue())
    """
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    i = 0
    count = 1
    while frontier:
        print(f'Step: {i}, Count: {count}')
        node = frontier.popleft()
        print(repr(node))
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                count += 1
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
        i += 1
    return None


def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    i = 0
    count = 1
    while frontier:
        print(f'Step: {i}, Count: {count}')
        node = frontier.pop()
        print(f"After : {node.action}")
        problem.printScoreHeuristic(node)
        print(f"Score : {f(node)}")
        print(repr(node))
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
                count += 1
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
        i += 1
    return None


def greedy_best_first_graph_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: h(n), display)


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: 0.3 * n.path_cost + 2 * (h(n) + 1), display)