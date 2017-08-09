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

        #  Generate occupancy object
        occ_obj = occ.Occupancy(number_occupants=nb_occ)

        #  Get radiation
        (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

        #  Generate stochastic electric power object
        el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                         total_nb_occ=nb_occ,
                                         q_direct=q_direct,
                                         q_diffuse=q_diffuse,
                                         is_sfh=False,
                                         prev_heat_dev=True,
                                         randomize_appliances=False,
                                         light_config=2,
                                         season_light_mod=True)
