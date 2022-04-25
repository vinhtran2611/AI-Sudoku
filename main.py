from fileinput import filename
from utils import *
from sudoku import *
from search import *
from datetime import datetime 
import tracemalloc


def run(grid, algorithm = "greedy"):
    initial = convert_to_tuple(grid)

    sudoku = Sudoku(initial= initial)
    print("Sloving...............")

    if(algorithm == 'dfs'):
        sol = depth_first_graph_search(sudoku)
    elif(algorithm == 'bfs'):
        sol = breadth_first_graph_search(sudoku)
    elif(algorithm == 'astar'):
        sol = astar_search(sudoku, display= True)
    elif(algorithm == 'greedy'):
        sol = greedy_best_first_graph_search(sudoku, display= True)
    else:
        print("Invalid algorithm or unsupported algorithm")
        return

    print("Done!!!!!!!.")
    if sol:
        print(sol.solution())
    else:
        print("No solution")

def main():
    
    

    #  run algorithm
    # filename = 'testcase/basic_03.txt'  
    filename = 'testcase/easy_01.txt'  
    # filename = 'testcase/intermediate_02.txt'  
    # filename = 'testcase/extreme_03.txt'  
    # filename = 'testcase/advanced_03.txt'  

    # starting the monitoring
    start_time = datetime.now() 
    tracemalloc.start()

    grid = read_file(filename=filename)
    demo = run(grid, 'astar')
    # dfs: 3p
    # bfs: 0:07:03.137449
    # greedy: 0:00:22.999490
    # a*: 0:00:17.883174


    time_elapsed = datetime.now() - start_time 

    print(f'Time execute: {time_elapsed}')
    print(f'Maximum memory used: {tracemalloc.get_traced_memory()[1]} KiB')
    tracemalloc.stop()
   

if __name__ == "__main__":
    main()