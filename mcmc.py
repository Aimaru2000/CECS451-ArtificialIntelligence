# Sydney Kao
# 017615869
# CECS 451 - 01
# Professor Moon
# Assignment 9

import random


def part_a():
    print('Part A. The sampling probabilities')
    # these numbers were double checked with bayes.jar
    print('P(C|-s,r) = <{0:.4f}, {1:.4f}>'.format(0.87805, 0.12195))
    print('P(C|-s,-r) = <{0:.4f}, {1:.4f}>'.format(0.31034, 0.68966))
    print('P(R|c, -s, w) = <{0:.4f}, {1:.4f}>'.format(0.9863, 0.0137))
    print('P(R|-c, -s, w) = <{0:.4f}, {1:.4f}>'.format(0.81818, 0.18182), end="\n\n")


def part_b():
    print('Part B. The transition probability matrix')

    # initialize the transition probability matrix
    rows = 4
    cols = 4
    tpm = [[0 for i in range(cols)] for j in range(rows)]

    # insert calculated values into the matrix
    tpm[0][0] = 0.9321
    tpm[0][1] = 0.0069
    tpm[0][2] = 0.0610
    tpm[0][3] = 0.0000
    tpm[1][0] = 0.4932
    tpm[1][1] = 0.1619
    tpm[1][2] = 0.0000
    tpm[1][3] = 0.3449
    tpm[2][0] = 0.4391
    tpm[2][1] = 0.0000
    tpm[2][2] = 0.4700
    tpm[2][3] = 0.0909
    tpm[3][0] = 0.0000
    tpm[3][1] = 0.1552
    tpm[3][2] = 0.4091
    tpm[3][3] = 0.4357

    # print the probabilities of each matrix
    print("\t\tS1\t\tS2\t\tS3\t\tS4")
    print('S1\t{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}'.format(tpm[0][0], tpm[0][1], tpm[0][2], tpm[0][3]))
    print('S2\t{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}'.format(tpm[1][0], tpm[1][1], tpm[1][2], tpm[1][3]))
    print('S3\t{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}'.format(tpm[2][0], tpm[2][1], tpm[2][2], tpm[2][3]))
    print('S4\t{0:.4f}\t{1:.4f}\t{2:.4f}\t{3:.4f}'.format(tpm[3][0], tpm[3][1], tpm[3][2], tpm[3][3]), end="\n\n")

    # for use in part c
    return tpm


def part_c(tpm):
    print('Part C. The probability for the query')

    # initialize the starting point
    current = random.randint(0, 3)

    # used to determine probability of P(c|-s,w)
    true_count = 0
    # used to determine probability of P(-c|-s,w)
    false_count = 0
    
    # number of times to loop
    n = 1000000

    for i in range(n):
        # this probability will determine if we will transition from the current state to another
        probability = random.uniform(0, 1)

        # determine the next state if current state is s1
        if current == 0:
            # stay at s1
            if probability < tpm[current][0]:
                true_count += 1
                current = 0
            # move to s2
            elif probability < tpm[current][0] + tpm[current][1]:
                true_count += 1
                current = 1
            # move to s3
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2]:
                false_count += 1
                current = 2

        # determine the next state if current state is s2
        elif current == 1:
            # move to s1
            if probability < tpm[current][0]:
                true_count += 1
                current = 0
            # stay at s2
            elif probability < tpm[current][0] + tpm[current][1]:
                true_count += 1
                current = 1
            # move to s4
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2] + tpm[current][3]:
                false_count += 1
                current = 3

        # determine the next state if current state is s3
        elif current == 2:
            # move to s1
            if probability < tpm[current][0]:
                true_count += 1
                current = 0
            # stay at s3
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2]:
                false_count += 1
                current = 2
            # move to s4
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2] + tpm[current][3]:
                false_count += 1
                current = 3

        # determine the next state if current state is s4
        else:
            # move to s2
            if probability < tpm[current][0] + tpm[current][1]:
                true_count += 1
                current = 1
            # move to s3
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2]:
                false_count += 1
                current = 2
            # stay at s4
            elif probability < tpm[current][0] + tpm[current][1] + tpm[current][2] + tpm[current][3]:
                false_count += 1
                current = 3

    true_probability = true_count / n
    false_probability = false_count / n
    
    print("P(C|-s, w) = <{0:.4f}, {1:.4f}>".format(true_probability, false_probability))


# print the outputs
if __name__ == '__main__':
    part_a()
    arr = part_b()
    part_c(arr)
