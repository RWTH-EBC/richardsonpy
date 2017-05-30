# coding=utf-8
"""
Example script for occupancy usage
"""

import numpy as np
import matplotlib.pyplot as plt

import richardsonpy.classes.occupancy as occ


def exampe_occupancy():

    #  Instanciate occupancy object
    occupancy_object = occ.Occupancy(number_occupants=3)

    #  Pointer to occupancy profile
    occupancy_profile = occupancy_object.occupancy

    print('Occupancy profile:')
    print(occupancy_profile)
    
    print('Maximum number of active occupants:')
    print(np.max(occupancy_profile))

    plt.figure()
    plt.plot(occupancy_object.occupancy[:200])
    plt.ylabel('Number of active occupants')
    plt.show()

if __name__ == '__main__':
    #  Run program
    exampe_occupancy()