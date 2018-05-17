#!/usr/bin/env python
# coding=utf-8
"""
Example script on how to generate a stochastic electric load profile
"""

import copy
import numpy as np
import matplotlib.pyplot as plt

import richardsonpy.classes.occupancy as occ
import richardsonpy.functions.change_resolution as cr
import richardsonpy.functions.load_radiation as loadrad
import richardsonpy.classes.electric_load as eload


def example_stoch_el_load(do_plot=False):
    #  Total number of occupants in apartment
    nb_occ = 3

    #  Generate occupancy object (necessary as input for electric load gen.)
    occ_obj = occ.Occupancy(number_occupants=nb_occ)

    #  Get radiation (necessary for lighting usage calculation)
    (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

    #  Generate stochastic electric power object
    el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                     total_nb_occ=nb_occ,
                                     q_direct=q_direct,
                                     q_diffuse=q_diffuse)

    #  Copy occupancy object, before changing its resolution
    #  (occ_obj.occupancy is the pointer to the occupancy profile array)
    occ_profile_copy = copy.copy(occ_obj.occupancy)

    #  Change resolution of occupancy object (to match 60 second timestep
    #  resolution of el. load profile; necessary for plotting)
    occ_profile_copy = cr.change_resolution(values=occ_profile_copy,
                                            old_res=600,
                                            new_res=60)

    if do_plot:
        #  Generate time array for plotting
        timesteps = 1440  # 60 second timesteps

        time_array = np.arange(0, timesteps * 60, 60) / 3600

        fig = plt.figure()
        fig.add_subplot(211)
        plt.plot(time_array, occ_profile_copy[0:timesteps])
        plt.xlabel('Timestep in hours')
        plt.ylabel('Number of active occupants')
        plt.xlim([0, 24])

        fig.add_subplot(212)
        plt.plot(time_array, el_load_obj.loadcurve[0:timesteps])
        plt.xlabel('Timestep in hours')
        plt.ylabel('Electric power in W')
        plt.xlim([0, 24])

        plt.tight_layout()
        plt.show()
        plt.close()


if __name__ == '__main__':
    example_stoch_el_load(do_plot=True)
