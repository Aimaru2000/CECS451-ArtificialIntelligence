# Sydney Kao
# CECS 451 - 01
# Professor Moon
# Spring 2022

# to report running time
import datetime
# from board.py
from board import Board
# for deep copying the board
import copy


# function that finds the best candidate
# f is the  original fitness
def candidate(f):
    current_fit = f
    best_fit = f

    # this is to avoid the local variable 'new_board' referenced before assignment error
    new_board = copy.deepcopy(board)

    for row in range(5):
        # we want deep copies so that the copies are independent from the parameter
        temp_board = copy.deepcopy(board)
        og_row = board.map[row]
        temp_board.map[row] = [0, 0, 0, 0, 0]
        for x in range(5):
            temp_board.flip(row, x)

            # compare the fitness of the current board and candidate board
            if og_row != temp_board.map[row] and 1 in temp_board.map[row]:
                fit = temp_board.get_fitness() - current_fit

                if fit < current_fit and fit < best_fit:
                    best_fit = fit
                    new_board = temp_board

                temp_board = copy.deepcopy(board)
                temp_board.map[row] = [0, 0, 0, 0, 0]

            else:
                temp_board.map[row][x] = 0
                x += 1

    return new_board


# function for implementation of hill climbing with a simple local search strategy
def hill_climbing(b):
    # we want deep copies so that the copies are independent from the parameter
    final_board = copy.deepcopy(b)
    fit = final_board.get_fitness()
    count = 0

    # while solution is not found...
    while fit != 0:
        temp_board = final_board
        # find the best candidate
        c = candidate(fit)

        # if the candidate = the fitness of the current board, return it
        if c.get_fitness() == temp_board.get_fitness():
            return final_board

        # otherwise, just choose the candidate and go from there
        final_board = copy.deepcopy(c)
        fit = c.get_fitness()
        count += 1

        # if we reach a certain count without finding the real solution, we will want to restart
        if count == 25:
            return final_board

    return final_board


# run the hill-climbing algorithm!
if __name__ == '__main__':
    # to count the number of restarts if algorithm gets stuck in local minima
    # if it doesn't get stuck, will output 0
    restarts = -1

    # to avoid possibility of output being undefined
    output = None

    # start counting time
    start_time = datetime.datetime.now()

    # to guarantee going through the algorithm at least once, initialize to -1
    final_fitness = -1

    while final_fitness != 0:
        board = Board(5)
        output = hill_climbing(board)
        final_fitness = output.get_fitness()
        restarts += 1

    # end counting time
    end_time = datetime.datetime.now()
    # convert to milliseconds
    timelapse = end_time - start_time
    timelapse2 = round((timelapse.total_seconds() * 1000), 2)

    print("Running Time: " + str(timelapse2) + "ms")

    print("Total Restarts: " + str(restarts))
    for x in range(0, 5):
        for y in range(0, 5):
            if output.map[x][y] == 0:
                print("-", end=' ')
            else:
                print(output.map[x][y], end=' ')
        print()
