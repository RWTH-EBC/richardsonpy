#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
richardsonpy: Package with Python version of Richardson tool

The Richardson tool is able to generate stochastic occupancy and electric load profiles for residential apartments.

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
Thomas Schuetz and
Jan Schiefelbein
Institute for Energy Efficient Buildings and Indoor Climate,
E.ON Energy Research Center,
RWTH Aachen University
"""

from setuptools import setup

setup(name='richardsonpy',
      version='0.2',
      description='Python version of Richardson tool to generate stochastic user and electric load profiles',
      url='https://github.com/RWTH-EBC/richardsonpy',
      author='Institute of Energy Efficient Buildings and Indoor Climate, '
             'E.ON Energy Research Center, RWTH Aachen University',
      license='GPL-3.0',
      packages=['richardsonpy'],
	  tests_require=['pytest'],
      install_requires=['numpy', 'matplotlib', 'xlrd'],
	  platforms='any',
	  classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
		  'Natural Language :: English',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'Topic :: Utilities'])
