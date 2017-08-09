#!/usr/bin/env python
# coding=utf-8
"""
Example script on how to generate a stochastic electric load profile
"""


import matplotlib.pyplot as plt

import richardsonpy.classes.occupancy as occ
import richardsonpy.functions.change_resolution as cr
import richardsonpy.functions.load_radiation as loadrad
import richardsonpy.classes.electric_load as eload


def example_stoch_el_load(do_plot=False):
    #  Total number of occupants in apartment
    nb_occ = 3

    #  Generate occupancy object
    occ_obj = occ.Occupancy(number_occupants=nb_occ)

    #  Get radiation
    (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

    #  Generate stochastic electric power object
    el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                     total_nb_occ=nb_occ,
                                     q_direct=q_direct, q_diffuse=q_diffuse)

    occ_profile = cr.change_resolution(values=occ_obj.occupancy,
                                      old_res=600,
                                      new_res=60)
    if do_plot:
        fig = plt.figure()
        fig.add_subplot(211)
        plt.plot(occ_profile[0:1440], label='occupancy')
        plt.xlabel('Timestep in minutes')
        plt.ylabel('Number of active occupants')

        fig.add_subplot(212)
        plt.plot(el_load_obj.loadcurve[0:1440], label='El. load')
        plt.xlabel('Timestep in minutes')
        plt.ylabel('Electric power in W')

        plt.tight_layout()
        plt.show()
        plt.close()


if __name__ == '__main__':
    example_stoch_el_load(do_plot=True)
