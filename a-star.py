# Sydney Kao
# Professor Moon
# CECS 451 Sec 01
# Spring 2022

import re
import math
import sys
from collections import deque

#############################
# PARSING TO CORRECT FORMAT #
#############################

# Function for reading map.txt and parsing it to an array
def read_map(filename):
    map_contents = []

    # use r to read the file only
    file = open(filename, "r")
    rows = file.readlines()

    # for each row, parse
    for i in range(len(rows)):
        columns = re.split(r'[-\s]\s*', rows[i])
        # remove the extra space at the end
        while '' in columns:
            columns.remove('')
        map_contents.append(columns)

    file.close()

    # the array is filled with contents from map.txt
    return map_contents


# Function to find child cities.
# @param cities is generated from read_map(map.txt)
def find_children(city_name, cities):
    city_names = [i[0] for i in cities]
    # print("city names")
    # print(city_names)

    # get the position of the city based on the index in the array
    index = city_names.index(city_name)
    # print(index)

    # using the position of the index, read city's connected cities
    connected_cities = cities[index]
    # print("connected cities")
    # print(connected_cities)

    # start at index 1 to avoid the parent city
    child_cities = re.split(r'[,()\s]', connected_cities[1])
    # remove extra spaces
    while '' in child_cities:
        child_cities.remove('')

    # in format [city, dist, city, dist...]
    return child_cities


# Function to group connected cities for the adjacent list
def group_children(children_list):
    city = []
    distance = []

    for i in children_list[::2]:
        city.append(i)
    for i in children_list[1::2]:
        # to fix the error of adding a str to an int
        distance.append(float(i))

    map = list(zip(city, distance))

    return map


# Function for reading coordinates.txt and parsing it to an array
def read_coordinates(filename):
    coor_contents = []

    # use r to read the file only
    file = open(filename, "r")
    rows = file.readlines()

    # for each row, parse
    for i in range(len(rows)):
        columns = re.split(r'[:\s]', rows[i])
        # remove the extra space at the end
        while '' in columns:
            columns.remove('')
        coor_contents.append(columns)

    file.close()

    # the array is filled with contents from coordinates.txt
    return coor_contents


# Function that returns the straight line distance between two cities using latitude and longitude
def find_straight_distance(lat1, lat2, long1, long2):
    # convert decimal to radians
    lat1rad = (lat1 * math.pi) / 180.0
    lat2rad = (lat2 * math.pi) / 180.0
    long1rad = (long1 * math.pi) / 180.0
    long2rad = (long2 * math.pi) / 180.0

    # calculate the differences for latitude and longitude (radians)
    lat_diff = lat2rad - lat1rad
    long_diff = long2rad - long1rad

    # Haversine formula
    a = math.sin(lat_diff / 2.0) ** 2.0 + math.cos(lat1rad) * math.cos(lat2rad) * math.sin(long_diff / 2.0) ** 2.0
    # print("a")
    # print(a)
    r = 3958.8
    dist = 2.0 * r * math.asin(math.sqrt(a))
    # print(dist)
    return dist


# Function to reformat so array becomes [city, straight distance to end, city, straight distance to end...]
# equivalent to h(n)
def reformat_straight_distance(end_city):
    read = read_coordinates('coordinates.txt')
    index = 0
    cities_list = []
    coordinates_list = []
    while index < len(read):
        city = read[index][0]
        add = read[index][1]
        cities_list.append(city)
        coordinates_list.append(add)
        index += 1

    index = 0
    new_cities = []
    while index < len(coordinates_list):
        values = re.split(r'[,()\s]', coordinates_list[index])
        while '' in values:
            values.remove('')
        new_cities.append(values)
        index += 1
    # print(cities_list)
    # print(new_cities)

    # find the index of the target end city
    index = 0
    while end_city != cities_list[index]:
        index += 1

    # print(index)
    # print(new_cities[1][0])

    # calculate the straight line distance between the city to the end city
    distance_list = []
    i = 0
    while i < len(new_cities):
        dist_temp = find_straight_distance(float(new_cities[i][0]), float(new_cities[index][0]),
                                           float(new_cities[i][1]), float(new_cities[index][1]))
        distance_list.append(dist_temp)
        i += 1
    # print(distance_list)

    # merge cities_list with distance_list in an alternating fashion
    merged_list = [None] * (len(cities_list) + len(distance_list))
    merged_list[::2] = cities_list
    merged_list[1::2] = distance_list

    return merged_list


# Function to group city to its corresponding heuristic for the adjacent list
def group_merged_list(merged_list):
    city = []
    h = []

    for i in merged_list[::2]:
        city.append(i)
    for i in merged_list[1::2]:
        # to fix the error of adding a str to an int
        h.append(float(i))

    map = dict(zip(city, h))

    return map


################
# A* ALGORITHM #
################

# a class that implements the a* algorithm
class Map:
    def __init__(self, list):
        self.list = list

    def get_children(self, v):
        return self.list[v]

    # uses the haversine function and functions defined above
    def heursitic(self, n, end_city):
        merged_list = reformat_straight_distance(end_city)
        heuristics = group_merged_list(merged_list)
        return heuristics[n]

    def a_star(self, start_city, end_city):
        # a history of the visited nodes, but neighbors have not been inspected
        open_list = set([start_city])

        # list of nodes that have been visited and inspected
        closed_list = set([])

        # distances from start_city to all visited cities
        # after undergoing the algorithm, calling g[end_city] will return the total distance of the path
        g = {}
        g[start_city] = 0

        # parents contain an adjacency map of all nodes
        parents = {}
        parents[start_city] = start_city

        while len(open_list) > 0:
            n = None

            # evaluation function f()
            for x in open_list:
                if n == None or g[x] + self.heursitic(x, end_city) < g[n] + self.heursitic(x, end_city):
                    n = x

            # Path does not exist
            if n == None:
                print("Path does not exist!")
                return None

            # if we reach the end city, construct the path
            if n == end_city:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.append(start_city)
                # path will result in reverse order, so we must reverse it in order for the path to be accurate
                path.reverse()
                # a path is found, so return it
                print("From city:", start_city)
                print("To city:", end_city)

                print("Best Route: ", end='')
                for i in range(len(path) - 1):
                    print(path[i] + " - ", end='')
                print(path[len(path)-1])

                dist = "{:.2f}".format(g[end_city])
                print(f"Total distance: {dist} mi")
                return path

            for (current, d) in self.get_children(n):
                # if the current city is not in open_list and closed_list
                # add it to the open_list and note n as its parent
                if current not in open_list and current not in closed_list:
                    open_list.add(current)
                    parents[current] = n
                    g[current] = g[n] + d

                # otherwise, check the distances and update the parent and g
                # if the city is in the closed_list, move it to the open_list
                else:
                    if g[current] > g[n] + d:
                        g[current] = g[n] + d
                        parents[current] = n

                        if current in closed_list:
                            closed_list.remove(current)
                            open_list.add(current)

            # remove n from the open_list and place it in closed_list because all children cities have been checked
            open_list.remove(n)
            closed_list.add(n)

        print("Path does not exist!")
        return None


#######################
# RUNNING THE PROGRAM #
#######################

reading = read_map('map.txt')

# create the cities to append to the adjancency_list
cities_list = []
for i in range(len(reading)):
    cities_list.append(reading[i][0])

# create the mapping of connected cities to the parent city
map_list = []
for i in range(len(cities_list)):
    temp = find_children(cities_list[i], reading)
    temp2 = group_children(temp)
    map_list.append(temp2)

# parsed version of map.txt
adjacency_list = dict(zip(cities_list, map_list))

# take input from console
input1 = sys.argv[1]
input2 = sys.argv[2]

# run the a* algorithm, and print the best route and total distance
graph1 = Map(adjacency_list)
graph1.a_star(input1, input2)