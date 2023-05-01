"""
robot.py:
    SCARA robot class
"""
import logging
import os

from .joint import Joint
from .tools.inverse_kinematic import inverse_kinematic
#from .tools.a_interaction import a_interaction
from .tools.manage_files import load_robot_config

logger = logging.getLogger(__name__)

class Robot():
    """
    Robot class
    """
    def __init__(self,
               config_file: str = "default"):
        logger.info("Initializing SCARA robot")
        self.config_file = config_file + ".yaml"
        abs_path = os.path.dirname(__file__)
        self.config_path = os.path.join(abs_path,
                                        "config",
                                        self.config_file)
        # load configuration
        joints, dimensions = load_robot_config(self.config_path)
        # joints
        self.hombro = Joint(odrv_serial_num=joints["hombro"]["odrv_serial_num"],
                            axis=joints["hombro"]["axis"],
                            config_file=config_file)
        self.codo = Joint(odrv_serial_num=joints["codo"]["odrv_serial_num"],
                          axis=joints["codo"]["axis"],
                          config_file=config_file)
        self.z = Joint(odrv_serial_num=joints["z"]["odrv_serial_num"],
                       axis=joints["z"]["axis"],
                       config_file=config_file)
        # dict with all joints
        self.all_joints = {"hombro": self.hombro,
                           "codo": self.codo,
                           "z": self.z}
        # dict with all home position per joint (joint's zero, not cartesian)
        self.all_pos_0 = {"hombro": self.hombro.pos_0,
                          "codo": self.codo.pos_0,
                          "z": self.z.pos_0}
        self.h_len = dimensions["humero_len"]
        self.rc_len = dimensions["radio_cubito_len"]
        self.max_hombro_degree = dimensions["max_hombro_degree"]
        self.max_codo_degree = dimensions["max_codo_degree"]
        self.cartesian_0 = dimensions["cartesian_0"]
        self.orientation = dimensions["orientation"]

    def setup(self):
        """
        Setup all joints
        """
        logger.info("Setup routine")
        for joint in self.all_joints.values():
            joint.j_setup()

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
