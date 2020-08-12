# -*- coding: utf-8 -*-
#!/usr/bin/env python
# twitter_bots/city

# created by Mario Rodríguez Chaves
# twitter: @mariuuuu5

import json     # read json files
import logging
import os
import random
from config import create_api

# set seed to get the same results
#random.seed(1)


MAPS_DIR = "./maps"                 # directory where the map grids are stored
BUILDINGS_FILE = "buildings.json"   # file where the buildings are stored

# lists of the different types of buildings
houses = ["🏠","🏡","🏘","🏢", "🏚"]
utilities	= ["🏨","🏦","🏥","🏤","🏣","🏬","🏫","🏩","💒"]
religious = ["⛪️","🕌","🕍"]
others 	= ["🏗","🎡","🏭","🏟","🗼", "🛕","🕋","⛩"]


houses_probs = [0.4, 0.6, 0.8, 0.95, 1]    # probability of each house to appear
other_probs = [0.8, 0.95, 1]              # probability of each type of building to appear (except houses)

# create logger and initialize it
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# TODO
# function that loads the buildings from a json file
def load_buildings():
    with open(BUILDINGS_FILE, 'r') as file:
        buildings = json.load(file)


# function that loads a random map from MAPS_DIR
def load_map():
    logger.info("Loading random map.")
    map_files = os.listdir(MAPS_DIR)                        # get a list of all the file names in the directory
    file_path = MAPS_DIR + "/" + random.choice(map_files)   # create the relative path to a random file
    logger.info(" Map selected: " + file_path)
    file = open(file_path, 'r')                             # open the file
    city_grid = file.read()                                 # read the map contained in the file and store it
    return city_grid                                        # return the map grid


# function that generates a random number [0-1) and gets the index
# of the first probability higher than that number
# probabilities must be a list of floats between 0 and 1 of increasing value
# for example if the probabilites list is [0.2, 0.6, 0.85, 1] and the
# random number is 0.45, then the function returns 1, the index of 0.6
def get_random_index(probabilities):
    found = False
    i = 0
    prob = random.random()
    
    while not found:
        if probabilities[i] >= prob:
            found = True
        else:
            i += 1
    return i

# function that generates the city based on the city grid
def generate_city(city_grid):
    logger.info("Generating city.")
    city = ""
    
    for building_type in city_grid.upper():         # for each character in the city grid
        if building_type == 'H':                    # if it is a house, it generates a random house building
            i = get_random_index(houses_probs)
            city += houses[i]
        elif building_type == 'R':                  # if it is a road, it generates a road or a vehicle
            prob = random.random()
            if prob < 0.1:
                city +="🚗"
            else:
                city += '     '
        else:                                       # else it copies de character (mainly for crlf)
            city += building_type
    
    logger.info("The city has been generated.")
    return city                                     # return the generated city


# function that tweets the city text
def send_city(api, city):
    api.update_status(city)
    logger.info("Tweet has been sent!")


def main():
    api = create_api()
    
    city_grid = load_map()
    city = generate_city(city_grid)
    send_city(api, city)


if __name__ == "__main__":
    main()