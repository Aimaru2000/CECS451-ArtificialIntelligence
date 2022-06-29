# Sydney Kao
# CECS 451 - 01
# Professor Moon
# Spring 2022

import random
# to report running time
import datetime
# from board.py
from board import Board
from math import comb


# function that creates the eight states
def eight_states():
    states = []
    row = [0, 0, 0, 0, 0]

    for i in range(8):
        for j in range(5):
            # randomized from 1 through 5 for each row
            row[j] = random.randint(1, 5)

        states.append(row)
        # reset the genes for the next iteration to use
        row = [0, 0, 0, 0, 0]

    return states


# function that maps the genes to the board
def map_genes(gene, b):
    b.map = [[0 for j in range(5)] for i in range(5)]
    for i in range(5):
        j = gene[i]
        b.map[i][j - 1] = 1
    return b


# function to find the fitness for the board
def gene_fitness(b):
    temp = b.get_fitness()
    h = comb(5, 2) - temp
    return h


# function that models the selection process for the genetic algorithm
def selection(eight_states):
    temp = Board(5)
    fitness = []
    selection = []

    # for each row, find the fitness and map the genes, add the fitness for future summing
    for row in range(8):
        fit = eight_states[row]
        current_board = map_genes(fit, temp)
        temp_fit = gene_fitness(current_board)
        if temp_fit == comb(5, 2):
            break
        fitness.append(temp_fit)

    fit_sum = sum(fitness)

    # get percentage
    percentage = [round(num/fit_sum, 2) for num in fitness]

    # select randomly based on the percentage
    for i in range(8):
        value = round(random.uniform(0, 1), 2)
        if value < float(sum(percentage[0:1])):
            selection.append(eight_states[0])
        elif value < float(sum(percentage[0:2])):
            selection.append(eight_states[1])
        elif value < float(sum(percentage[0:3])):
            selection.append(eight_states[2])
        elif value < float(sum(percentage[0:4])):
            selection.append(eight_states[3])
        elif value < float(sum(percentage[0:5])):
            selection.append(eight_states[4])
        elif value < float(sum(percentage[0:6])):
            selection.append(eight_states[5])
        elif value < float(sum(percentage[0:7])):
            selection.append(eight_states[6])
        else:
            selection.append(eight_states[7])

    return selection


# function that models the crossover step in the genetic algorithm
def crossover(eight_genes):
    cross = []

    first_half = eight_genes[0:4]
    second_half = eight_genes[4:8]

    # split in a random position for the pairs of genes
    for i in range(4):
        # position to split
        split = random.randint(1, 3)
        temp1 = first_half[i]
        temp2 = second_half[i]
        cross.append(temp1[:split] + temp2[split:])
        cross.append(temp2[:split] + temp1[split:])

    return cross


# function that models the mutation step in the genetic algorithm
def mutation(eight_genes):
    mutated = []

    # choose to mutate one number for each row
    for i in range(8):
        # position in the row
        position = random.randint(0, 4)
        # number for that particular position
        number = random.randint(1, 5)

        eight_genes[i][position] = number
        mutated.append(eight_genes[i])

    return mutated


# run the genetic algorithm!
if __name__ == '__main__':
    board = Board(5)
    # h is the number of attacking pairs
    h = 0

    genes = eight_states()

    # start counting time
    start_time = datetime.datetime.now()
    while h != comb(5, 2):
        for i in range(8):
            temp_board = map_genes(genes[i], board)
            h = gene_fitness(temp_board)

            # if solution is found
            if h == comb(5, 2):
                # end counting time
                end_time = datetime.datetime.now()
                # convert to milliseconds
                timelapse = end_time - start_time
                timelapse2 = round((timelapse.total_seconds() * 1000), 2)
                print("Running Time: " + str(timelapse2) + "ms")
                for x in range(0, 5):
                    for y in range(0, 5):
                        if temp_board.map[x][y] == 0:
                            print("-", end=' ')
                        else:
                            print(temp_board.map[x][y], end=' ')
                    print()
                break

            # else, run the genetic algorithm with the 4 different steps
            else:
                select = selection(genes)
                cross = crossover(select)
                mutate = mutation(cross)
                genes = mutate
