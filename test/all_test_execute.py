# coding=utf-8
"""
Code executes all pytests within test folder.

Please run all_test_execute.py before you push changes to repo and after
merging of branches.

Tests should terminate without error.
"""

import pytest

#  Calling all pytest, except energy balance test, as the fail for
#  regular pytest call
pytest.main()
