# Sydney Kao
# CECS 451 - 01
# Professor Moon
# Assignment 10

import sys


# function that reads the "cpt.txt" file
def read_file():
    arr = []
    with open(cpt) as f:
        for line in f:
            # remove the extra space at the end of each line
            line = line.strip('\n')
            arr.append(line)
    return arr


# function that calculates 1 - p and limits the decimal place to 2
def limit_double(p):
    z = 1.0 - float(p)
    limited = round(z, 2)
    return limited


# length is observation array length
# prob = probabilities matrix
# n = next_probability matrix
# e = e_probability matrix
# obs = observation array
def hmm(length, prob, n, e, obs):
    # This is most likely incorrect as it doesn't print out all P(Xt|e1:t) correctly...
    # I tried to follow what was given in the textbook/lecture slides as closely as I can
    # after the step for normalizing for t = 1, starting on day 2 of the example (reason why it's range(1, length))
    # Unfortunately, I am unsure how to implement using recursion so I used for loops instead
    for x in range(1, length):
        for y in range(2):
            # initialize a temp variable which will be used to update
            temp = 0
            # perform prediction from t-1 to t
            for z in range(2):
                temp += n[y][z] * prob[x - 1][z]
            # update evidence with time t considering the state of e
            prob[x][y] = temp * e[y][obs[x]]
    return prob


if __name__ == "__main__":
    # cpt is the second argument
    cpt = sys.argv[1]
    lines = read_file()

    # perform for each line in the "cpt.txt"
    for y in range(len(lines)):
        given = lines[y]
        x = lines[y].split(",")

        # The probability of P(x0)
        x0 = [float(x[0]), limit_double(x[0])]

        # The probability of the next X(t + 1) given the previous X(t)
        next_probability = [[float(x[1]), limit_double(x[1])], [float(x[2]), limit_double(x[2])]]

        # The probability of E given X at t
        e_probability = [[float(x[3]), limit_double(x[3])], [float(x[4]), limit_double(x[4])]]

        # observation results are put into a separate array
        # Assume that hidden state variable and evidence variable are binary variables.
        observation = []
        for i in range(5, len(x)):
            if x[i] == "f":
                observation.append(1)
            else:
                observation.append(0)

        # matrix for calculating P(X) at t, last row would be the result
        probabilities = [[0 for i in range(2)] for j in range(len(observation))]

        # step 1: update step simply multiplies by the probability of the evidence for t = 1 and normalizes
        probabilities[0][0] = x0[0] * e_probability[0][0]
        probabilities[0][1] = x0[1] * e_probability[1][0]
        normalize = sum(probabilities[0])
        probabilities[0][0] = probabilities[0][0] / normalize
        probabilities[0][1] = probabilities[0][1] / normalize

        # step 2: perform filtering by calling the function
        probabilities = hmm(len(observation), probabilities, next_probability, e_probability, observation)

        # step 3: normalize the final probabilities
        normalize = sum(probabilities[len(probabilities) - 1])
        probabilities[len(probabilities) - 1][0] = probabilities[len(probabilities) - 1][0] / normalize
        probabilities[len(probabilities) - 1][1] = probabilities[len(probabilities) - 1][1] / normalize

        print(given, end='')
        print('--><{0:.4f}, {1:.4f}>'.format(probabilities[len(probabilities) - 1][0],
                                             probabilities[len(probabilities) - 1][1]))
