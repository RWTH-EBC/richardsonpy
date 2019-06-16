[![Build Status](https://travis-ci.org/RWTH-EBC/richardsonpy.svg?branch=master)](https://travis-ci.org/RWTH-EBC/richardsonpy.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/RWTH-EBC/richardsonpy/badge.svg?branch=master)](https://coveralls.io/github/RWTH-EBC/richardsonpy?branch=master)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# richardsonpy
Python version of Richardson tool

Original version published under GNU GENERAL PUBLIC LICENSE by
Ian Richardson,
Murray Thomson and
David Infield
CREST (Centre for Renewable Energy Systems Technology),
Department of Electronic and Electrical Engineering,
Loughborough University, Leicestershire LE11 3TU, UK
and
Department of Electronic & Electrical Engineering, University of Strathclyde,
UK
Tel. +44 1509 635326. Email address: I.W.Richardson@lboro.ac.uk				

see: 

https://dspace.lboro.ac.uk/dspace-jspui/handle/2134/3112

and

https://dspace.lboro.ac.uk/dspace-jspui/handle/2134/5786

Python version provided by:
Institute for Energy Efficient Buildings and Indoor Climate,
E.ON Energy Research Center,
RWTH Aachen University


## Installation

Installation is possible via pip:

'pip install richardsonpy'
(for static installation into your current Python distribution)

or

clone development version via git and install via pip (egglink):
'pip install -e <your_path_to_richardsonpy>'

## Dependencies

richardsonpy requires the following Python packages:
- numpy
- matplotlib
- xlrd

##  Example usage

Example code on how to generate a stochastic user profile (profile of active occupancy; 600 seconds resolution)

```Python
import numpy as np

import richardsonpy.classes.occupancy as occ

#  Total number of occupants within apartment
number_occupants = 3

#  Generate occupancy object instance
occupancy_object = occ.Occupancy(number_occupants=number_occupants)

#  Pointer to occupancy profile
occupancy_profile = occupancy_object.occupancy
```

Example code on how to generate stochastic electric load profile (60 seconds resolution)

```Python
import richardsonpy.classes.occupancy as occ
import richardsonpy.functions.change_resolution as cr
import richardsonpy.functions.load_radiation as loadrad
import richardsonpy.classes.electric_load as eload


def example_stoch_el_load():
    #  Total number of occupants in apartment
    nb_occ = 3

    timestep = 60  # in seconds

    #  Generate occupancy object (necessary as input for electric load gen.)
    occ_obj = occ.Occupancy(number_occupants=nb_occ)

    #  Get radiation (necessary for lighting usage calculation)
    (q_direct, q_diffuse) = loadrad.get_rad_from_try_path()

    #  Convert 3600 s timestep to given timestep
    q_direct = cr.change_resolution(q_direct, old_res=3600, new_res=timestep)
    q_diffuse = cr.change_resolution(q_diffuse, old_res=3600, new_res=timestep)

    #  Generate stochastic electric load object instance
    el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                     total_nb_occ=nb_occ,
                                     q_direct=q_direct,
                                     q_diffuse=q_diffuse,
                                     timestep=timestep)

    #  Calculate el. energy in kWh by accessing loadcurve attribute
    energy_el_kwh = sum(el_load_obj.loadcurve) * timestep / (3600 * 1000)

    print('Electric energy demand in kWh: ')
    print(energy_el_kwh)

if __name__ == '__main__':
    example_stoch_el_load()
```

##  Basic input data sets

The appliance data, light bulb configurations, transition probability matrices,
activity statistics, and weather data can be found in
...\richardsonpy\inputs\...

In case you want to use own customized data sets,
for instance for appliances: 
Copy and modify Appliances.csv 
and provide the new path for the ElectricLoad object,
e.g.:
```Python
#  Generate stochastic electric load object instance
    el_load_obj = eload.ElectricLoad(occ_profile=occ_obj.occupancy,
                                     total_nb_occ=nb_occ,
                                     q_direct=q_direct,
                                     q_diffuse=q_diffuse,
                                     path_app=your_path_to_app_csv)
```

Furter input parameters for the constructor of the
ElectricLoad object instance are:
```Python
    def __init__(self, occ_profile, total_nb_occ, q_direct, q_diffuse,
                 annual_demand=None, is_sfh=True,
                 path_app=None, path_light=None, randomize_appliances=True,
                 prev_heat_dev=False, light_config=0, timestep=60,
                 initial_day=1,
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
        timestep : int, optional
            Timestep for profile rescaling (default: 60). Profile is
            originally generated with 60 seconds timestep. If another
            timestep is given, profile resolution is changed to given
            timestep.
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
```

##  References

[1] I. Richardson, M. Thomson, D. Infield, 
A high-resolution domestic building occupancy model for energy demand simulations, 
Energy and Buildings 40 (8) (2008) 1560 1566.

[2] I. Richardson, M. Thomson, D. Infield, A. Delahunty, 
Domestic lighting: A high-resolution energy demand model, 
Energy and Buildings 41 (7) (2009) 781 789.

[3] I. Richardson, M. Thomson, D. Infield, C. Clifford, 
Domestic electricity use: A high-resolution energy demand model, 
Energy and Buildings 42 (10) (2010) 1878 1887.


## License

richardsonpy is released by RWTH Aachen University's Institute for Energy Efficient Buildings and Indoor Climate (EBC) 
under the [GNU GENERAL PUBLIC LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Acknowledgements

Grateful acknowledgement is made for financial support by Federal Ministry for Economic Affairs and Energy (BMWi), 
promotional references 03ET1138D.

<img src="http://www.innovation-beratung-foerderung.de/INNO/Redaktion/DE/Bilder/Titelbilder/titel_foerderlogo_bmwi.jpg;jsessionid=4BD60B6CD6337CDB6DE21DC1F3D6FEC5?__blob=poster&v=2)" width="200">

Moreover, we would like to thank Ian Richardson, Murray Thomson and David 
Infield for providing the basic tool version as open-source tool.