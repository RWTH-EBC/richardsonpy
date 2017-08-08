# coding=utf-8

from __future__ import division

import richardsonpy.functions.change_resolution as chres


class Test_ChangeResolution(object):
    """
    Test class for change of resolution functions
    """

    def test_change_res_mean_larger_timestep(self):
        input_array = [10, 10, 20, 20]
        output_array = chres.change_resolution(values=input_array,
                                                old_res=900,
                                                new_res=3600,
                                                method="mean")
        assert output_array[0] == 10

    def test_change_res_mean_larger_timestep_2(self):
        input_array = [10, 20, 20, 20, 20, 30]
        output_array = chres.change_resolution(values=input_array,
                                                old_res=900,
                                                new_res=3600,
                                                method="mean")
        assert output_array[0] == 10
        assert output_array[1] == 20


    def test_change_res_mean_smaller_timestep(self):
        input_array = [10, 20]
        output_array = chres.change_resolution(values=input_array,
                                                old_res=3600,
                                                new_res=900,
                                                method="mean")
        assert output_array[0] == 10
        assert output_array[1] == 12.5
        assert output_array[2] == 15.
        assert output_array[3] == 17.5
        assert output_array[4] == 20
        assert output_array[5] == 20
        assert output_array[6] == 20
        assert output_array[7] == 20

    def test_change_res_sum_larger_timestep(self):
        input_array = [10, 10, 20, 20]
        output_array = chres.change_resolution(values=input_array,
                                                old_res=900,
                                                new_res=3600,
                                                method="sum")
        assert output_array == [60]

    def test_change_res_sum_smaller_timestep(self):
        input_array = [10, 20]
        output_array = chres.change_resolution(values=input_array,
                                                old_res=3600,
                                                new_res=900,
                                                method="sum")
        assert output_array[0] == 2.5
        assert output_array[1] == 2.5
        assert output_array[2] == 2.5
        assert output_array[3] == 2.5
        assert output_array[4] == 5
        assert output_array[5] == 5
        assert output_array[6] == 5
        assert output_array[7] == 5
