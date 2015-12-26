__author__ = 'gabib3b'
from enum import Enum
from random import randint

class LocationType(Enum):
    Sea = 1
    Park = 2
    CityCEnter = 3
    Highway = 4
    Suburb = 5

class PreferenceProbabilityGroup():

    def __init__(self, from_index, to_index, from_value, to_value):
        self._from_index = from_index
        self._to_index = to_index
        self._from_value = from_value
        self._to_value = to_value

    def start_index(self):
        return self._from_index

    def end_index(self):
        return self._to_index

    def max_value(self):
        return self._to_value

    def min_value(self):
        return self._from_value



class LocationTypeIndex:

    def __init__(self, distance, location_type):
        self._distance = distance
        self._location_type = location_type

    def locationType(self):
        return self._location_type

    def locationDistance(self):
        return self._distance



"""
   :return: map of distance from special location to its influence means
    0 we are in the location so the influence is 100%
    1 index near so 0.8
    2 two indexes so 0.6
    etc...
"""
def LOCATION_INFLUENCE_DISTANCE():
    return  {0:1, 1:0.8, 2:0.6, 3:0.5, 4:0.2, 5:0.1}


def LOCATION_TYPES():
    allLocations = []

    allLocations.append(LocationType.CityCEnter)
    allLocations.append(LocationType.Highway)
    allLocations.append(LocationType.Park)
    allLocations.append(LocationType.Sea)
    allLocations.append(LocationType.Suburb)

    return allLocations

def SPECIAL_LOCATIONS_PERCENTAGE():
    return 0.1

def index_to_location_type(mean_values, locations_type):

    index_to_location_type_map = {}

    special_location_percentage = SPECIAL_LOCATIONS_PERCENTAGE()

    for i in range(len(mean_values)):

        if mean_values[i] > 0:
            rand_value = randint(1, 10)
            selected_rand_index = 10 * special_location_percentage
            if rand_value <= selected_rand_index:
                index_to_location_type_map[i] = LocationTypeIndex(0, _select_special_location_randomly(locations_type))


    distance_index_map ={}
    location_influence_map = LOCATION_INFLUENCE_DISTANCE()
    distance_indexes = location_influence_map.keys()
    for index, location_type_index in index_to_location_type_map.items():

        for dis_index in distance_indexes:

            if dis_index == 0:
                continue

            before_index = index - dis_index
            after_index = index + dis_index

            if before_index not in index_to_location_type_map:
                existing_distance_index = None
                if before_index in distance_index_map:
                    existing_distance_index = distance_index_map[before_index]

                if existing_distance_index is None or (dis_index < existing_distance_index.locationDistance()):
                    distance_index_map[before_index] = LocationTypeIndex(dis_index, location_type_index.locationType())

                if after_index not in index_to_location_type_map:
                    existing_distance_index = None
                    if after_index in distance_index_map:
                        existing_distance_index = distance_index_map[after_index]

                if existing_distance_index is None or (dis_index < existing_distance_index.locationDistance()):
                    distance_index_map[after_index] = LocationTypeIndex(dis_index, location_type_index.locationType())



    index_to_location_type_map.update(distance_index_map.items())
    return index_to_location_type_map


def _select_special_location_randomly(locations_type):
    rand_value = randint(0, len(locations_type) - 1)
    return locations_type[rand_value]

def PREFERENCES_PROBABILITY_GROUPS():
    preferences_indexes = []
    preferences_indexes.append(PreferenceProbabilityGroup(0, 4, 0.1, 0.5))
    preferences_indexes.append(PreferenceProbabilityGroup(4, 6, 0.6, 1))
    preferences_indexes.append(PreferenceProbabilityGroup(6, 7, 1.1, 2))
    preferences_indexes.append(PreferenceProbabilityGroup(7, 11,-0.5, 0))
    preferences_indexes.append(PreferenceProbabilityGroup(11, 12 ,-0.8, -0.6))
    preferences_indexes.append(PreferenceProbabilityGroup(12, 16 ,0, 0))

    return preferences_indexes






