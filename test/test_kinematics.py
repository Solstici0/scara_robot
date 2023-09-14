import pytest
import scara.tools.kinematics as kin

def test_correct_import():
    assert  330.15  == kin.dimensions['humero_len']