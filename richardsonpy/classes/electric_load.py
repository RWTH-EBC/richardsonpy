#!/usr/bin/env python
# coding=utf-8
"""
Script holding ElectricLoad class
"""
from __future__ import division

import os
import numpy as np

import richardsonpy.classes.appliance as app_model
import richardsonpy.classes.lighting as light_model
import richardsonpy.classes.stochastic_el_load_wrapper as wrapper
import richardsonpy.functions.change_resolution as cr
import richardsonpy.functions.load_radiation as loadrad


class ElectricLoad(object):
    """
    Electric load class
    """

    #  Used, if no annual el. demands are handed over / annual_demand is set
    #  to zero.
    standard_consumption = {"SFH": {1: 2700,
                                    2: 3200,
                                    3: 4000,
                                    4: 4400,
                                    5: 5500},
                            "MFH": {1: 1500,
                                    2: 2200,
                                    3: 3000,
                                    4: 3400,
                                    5: 4100}}

    def __init__(self, occ_profile, total_nb_occ, q_direct, q_diffuse,
                 annual_demand=None, is_sfh=True,
                 path_app=None, path_light=None, randomize_appliances=True,
                 prev_heat_dev=False, light_config=0, initial_day=1,
                 season_light_mod=False,
                 light_mod_fac=0.25, do_normalization=False, calc_profile=True,
                 save_app_light=False):
        """
        Constructor of ElectricLoad class

        Parameters
        ----------
        occ_profile : array-like
            Occupancy profile given at 10-minute intervals for a full year
        total_nb_occ : int
            Maximum possible number of occupants (does not necessarily need to
            be equal to max(occ_profile), as there is no guarantee, that
            maximum number of persons is reached
        q_direct : array-like
            Direct radiation in kW/m2
        q_diffuse : array-like
            Diffuse radiation in kW/m2
        annual_demand : float, optional
            Annual electric energy demand in kWh
        is_sfh : bool, optional
            Defines, if building type is of type single family house
            (default: True). If False, assumes multi-family house.
        path_app : str, optional
            Path to appliance input data set (default: None). If None, uses
            ...\richardsonpy\richardsonpy\inputs\Appliances.csv
        path_light : str, optional
            Path to lighting input data set (default: None). If None, uses
            ...\richardsonpy\richardsonpy\inputs\LightBulbs.csv
        randomize_appliances : bool, optional
            Defines, if random set of appliance should be selected
            (default: True). If False, always uses defined appliances in
            ...\richardsonpy\richardsonpy\inputs\Appliances.csv
        prev_heat_dev : bool, optional
            Enables prevention of electric heating devices and hot water
            devices (default: False). If True, devices for space heating and
            hot water are not allowed to be installed.
        light_config : int, optional
            Number of lighting configuration (default: 0)
        initial_day : int, optional
            Defines number for initial weekday (default: 1).
            1-5 correspond to Monday-Friday, 6-7 to Saturday and
            Sunday
        season_light_mod : bool, optional
            Defines, if sinus-wave should be used to modify electric load
            profile to account for seasonal influence, mainly lighting
            differences in summer and winter month (default: False)
        light_mod_fac : float optional
            Modification factor for season_light_mod == True (default: 0.25)
        do_normalization : bool optional
            Defines, if profile should be normalized to given annual electric
            reference demand value in kWh (default: False)
        calc_profile : bool, optional
            Defines, if profile should be generated (default: True).
        save_app_light : bool, optional
            Defines, if separate electric profiles for appliance and lighting
            should be saved (default: False). If False, only saves summed up
            electric load profiles.

        Returns
        -------
        loadcurve : array-like
            Electric power load curve in W
        """

        assert total_nb_occ > 0
        if total_nb_occ > 5:
            msg = 'Implementation of probability matrices does only account' \
                  ' for apartments with up to 5 persons per apartment. ' \
                  'Please select a lower number of occupants!'
            raise AssertionError(msg)

        self.occ_profile = occ_profile  # Occupancy object
        self.total_nb_occ = total_nb_occ  # Total number of occupants
        self.annual_demand = annual_demand  # Annnual el. demand in kWh
        self.appliances = None  # Appliances object
        self.lights = None  # Lighting object
        self.wrapper = None  # Stoch. el. load wrapper

        self.light_load = None  # Lighting profile in W
        self.app_load = None  # Appliance power profile in W
        self.loadcurve = None  # El. power profile in W

        self._timestep = 60  # in seconds
        self._timestep_try = 3600  # in seconds

        if calc_profile:
            self.calc_stoch_el_profile(q_direct=q_direct, q_diffuse=q_diffuse,
                                       is_sfh=is_sfh, path_app=path_app,
                                       path_light=path_light,
                                       randomize_appliances=randomize_appliances,
                                       prev_heat_dev=prev_heat_dev,
                                       light_config=light_config,
                                       initial_day=initial_day,
                                       season_light_mod=season_light_mod,
                                       light_mod_fac=light_mod_fac,
                                       do_normalization=do_normalization,
                                       save_app_light=save_app_light)

    def calc_stoch_el_profile(self, q_direct, q_diffuse, is_sfh=True,
                              path_app=None, path_light=None,
                              randomize_appliances=True,
                              prev_heat_dev=False, light_config=0,
                              initial_day=1, season_light_mod=False,
                              light_mod_fac=0.25,
                              do_normalization=False,
                              save_app_light=False):
        """

        Parameters
        ----------
        q_direct : array-like
            Direct radiation in kW/m2
        q_diffuse : array-like
            Diffuse radiation in kW/m2
        is_sfh : bool, optional
            Defines, if building type is of type single family house
            (default: True). If False, assumes multi-family house.
        path_app : str, optional
            Path to appliance input data set (default: None). If None, uses
            ...\richardsonpy\richardsonpy\inputs\Appliances.csv
        path_light : str, optional
            Path to lighting input data set (default: None). If None, uses
            ...\richardsonpy\richardsonpy\inputs\LightBulbs.csv
        randomize_appliances : bool, optional
            Defines, if random set of appliance should be selected
            (default: True). If False, always uses defined appliances in
            ...\richardsonpy\richardsonpy\inputs\Appliances.csv
        prev_heat_dev : bool, optional
            Enables prevention of electric heating devices and hot water
            devices (default: False). If True, devices for space heating and
            hot water are not allowed to be installed.
        light_config : int, optional
            Number of lighting configuration (default: 0)
        initial_day : int, optional
            Defines number for initial weekday (default: 1).
            1-5 correspond to Monday-Friday, 6-7 to Saturday and
            Sunday
        season_light_mod : bool, optional
            Defines, if sinus-wave should be used to modify electric load
            profile to account for seasonal influence, mainly lighting
            differences in summer and winter month (default: False)
        light_mod_fac : float optional
            Modification factor for season_light_mod == True (default: 0.25)
        do_normalization : bool optional
            Defines, if profile should be normalized to given annual electric
            reference demand value in kWh (default: False)
        save_app_light : bool, optional
            Defines, if separate electric profiles for appliance and lighting
            should be saved (default: False). If False, only saves summed up
            electric load profiles.
        """

        this_path = os.path.dirname(os.path.abspath(__file__))

        src_path = os.path.dirname(this_path)

        if path_app is None:  # Use default
            path_app = os.path.join(src_path, 'inputs', 'Appliances.csv')

        if path_light is None:  # Use default
            path_light = os.path.join(src_path, 'inputs', 'LightBulbs.csv')

        # Initialize appliances and lights
        if self.annual_demand is None:

            if is_sfh:
                self.annual_demand = \
                    self.standard_consumption["SFH"][self.total_nb_occ]
            else:
                self.annual_demand = \
                    self.standard_consumption["MFH"][self.total_nb_occ]

        # According to http://www.die-stromsparinitiative.de/fileadmin/
        # bilder/Stromspiegel/Brosch%C3%BCre/Stromspiegel2014web_final.pdf
        # roughly 9% of the electricity consumption are due to lighting.
        # This has to be excluded from the appliances' demand:
        appliancesDemand = 0.91 * self.annual_demand

        #  Get appliances
        self.appliances = \
            app_model.Appliances(path_app,
                                 annual_consumption=appliancesDemand,
                                 randomize_appliances=randomize_appliances,
                                 prev_heat_dev=prev_heat_dev)

        #  Get lighting configuration
        self.lights = light_model.load_lighting_profile(filename=path_light,
                                                        index=light_config)

        # Create wrapper object
        timestepsDay = int(86400 / self._timestep_try)
        self.wrapper = wrapper.ElectricityProfile(self.appliances,
                                                  self.lights)

        # Make full year simulation
        demand = []
        light_load = []
        app_load = []

        irradiance = q_direct + q_diffuse
        required_timestamp = np.arange(1440)
        given_timestamp = self._timestep * np.arange(timestepsDay)

        # Loop over all days
        for i in range(int(len(irradiance) * self._timestep_try / 86400)):
            if (i + initial_day) % 7 in (0, 6):
                weekend = True
            else:
                weekend = False

            irrad_day = irradiance[
                        timestepsDay * i: timestepsDay * (i + 1)]
            current_irradiation = np.interp(required_timestamp,
                                            given_timestamp, irrad_day)

            current_occupancy = self.occ_profile[144 * i: 144 * (i + 1)]

            (el_p_curve, light_p_curve, app_p_curve) = \
                self.wrapper.demands(current_irradiation,
                                     weekend,
                                     i,
                                     current_occupancy)

            demand.append(el_p_curve)
            light_load.append(light_p_curve)
            app_load.append(app_p_curve)

        res = np.array(demand)
        light_load = np.array(light_load)
        app_load = np.array(app_load)

        res = np.reshape(res, res.size)
        light_load = np.reshape(light_load, light_load.size)
        app_load = np.reshape(app_load, app_load.size)

        if season_light_mod:
            #  Put cosine-wave on lighting over the year to estimate
            #  seasonal influence

            light_energy = sum(light_load) * 60

            time_array = np.arange(start=0, stop=len(app_load))
            time_pi_array = time_array * 2 * np.pi / len(app_load)

            cos_array = 0.5 * np.cos(time_pi_array) + 0.5

            ref_light_power = max(light_load)

            light_load_new = np.zeros(len(light_load))

            for i in range(len(light_load)):
                if light_load[i] == 0:
                    light_load_new[i] = 0
                elif light_load[i] > 0:
                    light_load_new[i] = light_load[i] + \
                                        light_mod_fac * ref_light_power \
                                        * cos_array[i]

            light_energy_new = sum(light_load_new) * 60

            #  Rescale to original lighting energy demand
            light_load_new *= light_energy / light_energy_new

            res = light_load_new + app_load

        # Change time resolution
        loadcurve = cr.change_resolution(res, 60, self._timestep)
        light_load = cr.change_resolution(light_load, 60, self._timestep)
        app_load = cr.change_resolution(app_load, 60, self._timestep)

        #  Normalize el. load profile to annual_demand
        if do_normalization:
            #  Convert power to energy values
            energy_curve = loadcurve * self._timestep  # in Ws

            #  Sum up energy values (plus conversion from Ws to kWh)
            curr_el_dem = sum(energy_curve) / (3600 * 1000)

            con_factor = self.annual_demand / curr_el_dem

            #  Rescale load curves
            loadcurve *= con_factor
            light_load *= con_factor
            app_load *= con_factor

        if save_app_light:
            self.light_load = light_load
            self.app_load = app_load

        self.loadcurve = loadcurve


if __name__ == '__main__':
    #  Total number of occupants in apartment
    nb_occ = 3

    import richardsonpy.classes.occupancy as occ

    #  Generate occupancy object
    occ_obj = occ.Occupancy(number_occupants=nb_occ)

    #  Get radiation
    (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

    #  Generate stochastic electric power object
    el_load_obj = ElectricLoad(occ_profile=occ_obj.occupancy,
                               total_nb_occ=nb_occ,
                               q_direct=q_direct, q_diffuse=q_diffuse)

    occ_profile = cr.change_resolution(values=occ_obj.occupancy,
                                      old_res=600,
                                      new_res=60)

    import matplotlib.pyplot as plt

    fig = plt.figure()
    fig.add_subplot(211)
    plt.title('Occupancy and electric load for 24 hours')
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

    print(len(el_load_obj.loadcurve))

    fig = plt.figure()
    fig.add_subplot(211)
    plt.title('Annual occupancy and electric load profiles')
    plt.plot(occ_profile, label='occupancy')
    plt.xlabel('Timestep in minutes')
    plt.ylabel('Number of active occupants')

    fig.add_subplot(212)
    plt.plot(el_load_obj.loadcurve, label='El. load')
    plt.xlabel('Timestep in minutes')
    plt.ylabel('Electric power in W')

    plt.tight_layout()
    plt.show()
    plt.close()

    sum_el_energy = sum(el_load_obj.loadcurve) * 60 / 3600000
    print('Electric energy in kWh: ', sum_el_energy)
