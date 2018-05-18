#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import richardsonpy.classes.occupancy as occ
import richardsonpy.functions.change_resolution as cr
import richardsonpy.functions.load_radiation as loadrad
import richardsonpy.classes.electric_load as eload


class Test_eload_with_heat_dev():


    def test_eload_w_heat(self):
        #  Total number of occupants in apartment
        nb_occ = 5

        timestep = 60

        #  Generate occupancy object
        occ_obj = occ.Occupancy(number_occupants=nb_occ)

        #  Get radiation
        (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

        #  Convert 3600 s timestep to given timestep
        q_direct = cr.change_resolution(q_direct, old_res=3600,
                                        new_res=timestep)
        q_diffuse = cr.change_resolution(q_diffuse, old_res=3600,
                                         new_res=timestep)

        #  Generate stochastic electric power object
        el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                         total_nb_occ=nb_occ,
                                         q_direct=q_direct,
                                         q_diffuse=q_diffuse,
                                         is_sfh=False,
                                         prev_heat_dev=True,
                                         randomize_appliances=False,
                                         light_config=2,
                                         season_light_mod=True,
                                         timestep=timestep)
