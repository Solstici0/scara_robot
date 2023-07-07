import pytest

import scara


@pytest.fixture(scope='session')
def nelen():
    robot_object = scara.Robot()
    return robot_object

def test__initialize_robot__succeed(nelen):
    assert nelen.is_initialized == True

def test__setup_robot__succeed(nelen):
    nelen.setup()
    assert nelen.is_setted_up == True

def test__move2_robot_wo_a__succeed(nelen):
    nelen.move2(x=3,
                y=5,
                z=1)

def test__move2_robot_w_a__succeed(nelen):
    nelen.move2(x=3,
                y=5,
                z=1,
                a=0.5)
