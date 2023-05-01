"""
fake_odrive.py:
    fake Odrive for debugging porpuse
"""
import logging

logger = logging.getLogger(__name__)

def find_any():
    logger.debug("Finding FakeOdrv")
    return FakeOdrv()

def dump_errors(odrv, verbose):
    logger.debug("Fake Dump_errors")

class FakeOdrv():
    """
    FakeOdrv class
    """
    def __init__(self):
        logger.debug("init FakeOdrv")

    def axis0(self):
        logger.debug("returning FakeOdrv.axis0")
        return FakeJoint()

    def axis1(self):
        logger.debug("returning FakeOdrv.axis1")
        return FakeJoint()


class FakeJoint():
    """
    FakeJoint class
    """
    def __init__(self, initial_state=1):
        logger.debug("creating FakeOdrv.FakeJoint")
        self.requested_state = initial_state
        self.current_state = initial_state
        self.controller = FakeController()

    @property
    def requested_state(self):
        logger.debug("property FakeOdrv.FakeJoint.requested_state")
        return self._requested_state

    # Update current_state whenever requested_state changes
    @requested_state.setter
    def requested_state(self, value):
        logger.debug("setter FakeOdrv.FakeJoint.requested_state")
        self._requested_state = value
        self.current_state = value


class FakeController():
    """
    FakeController
    """
    def __init__(self):
        logger.debug("creating FakeOdrv.FakeJoint.Controller")

    def move_incremental(self, pos_increment, from_goal_point):
        logger.debug("move_incremental FakeOdrv.FakeJoint.Controller")
        pass
