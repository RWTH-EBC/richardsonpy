#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import division

import richardsonpy.examples.example_el_load as eload
import richardsonpy.examples.example_occupancy as occex

class Test_RunExamples():
    def test_example_el_load(self):
        eload.example_stoch_el_load()

    def test_example_occupancy(self):
        occex.exampe_occupancy()
