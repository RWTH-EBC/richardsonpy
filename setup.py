#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
richardsonpy: Package with Python version of Richardson tool

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

see: https://dspace.lboro.ac.uk/dspace-jspui/handle/2134/3112

Python version provided by:
Thomas Schütz and
Jan Schiefelbein
RWTH Aachen University, E.ON Energy Research Center,
Institute for Energy Efficient Buildings and Indoor Climate
"""

from setuptools import setup



setup(name='richardsonpy',
      version='0.1',
      description='Python version of Richardson tool',
      url='https://github.com/RWTH-EBC/richardsonpy',
      author='RWTH Aachen University, E.ON Energy Research Center, '
             'Institute of Energy Efficient Buildings and Indoor Climate',
      author_email='ebc-teaser@eonerc.rwth-aachen.de',
      license='GPL-3.0',
      packages=['richardsonpy'],
      install_requires=['numpy', 'matplotlib', 'xlrd', 'pandas'])
