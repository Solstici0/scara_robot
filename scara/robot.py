"""
robot.py:
    SCARA robot class
"""
import logging

from .joint import Joint
from .tools import inverse_kinematic, \
                   a_interaction

logger = logging.getLogger(__name__)

class Robot():
    """
    Robot class
    """
    def __init__(self,
               config_path: str = '.'):
        logger.info("Initializing SCARA robot")
        #hombro_axis, codo_axis, z_axis, humero_len, radio-cubito_len =
        #load_config(config_path)
        #self.hombro = Joint(hombro_axis)
        #self.codo = Joint(codo_axis)
        #self.z = Joint(z_axis)
        #self.h_len = humero_len
        #self.rc_len = radio-cubito_len
        pass

    def setup(self):
        """
        """
        logger.info("Setup routine")
        #TODO this routine should be sequential
        #self.joint.j_setup()
        pass

    def go_home(self):
        """
        """
        logger.info("Doing homing routine")
        #self.joint.j_move2(joint_pos_0)
        pass

    def move2(self,
            x: float,
            y: float,
            z: float,
            mode: str):
        """
        """
        logger.info("Moving to position x: %.2f, y: %.2f, z: %.2f in %s mode",
                    x,
                    y,
                    z,
                    mode)
        #TODO should be possible to do it in  parallel
        #theta_1, theta_2 = inverse_kinematic(x, y, self.h_len, self.rc_len)
        #self.joint.j_move2(joint_pos)
        pass
