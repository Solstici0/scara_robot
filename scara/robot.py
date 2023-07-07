"""
robot.py:
    SCARA robot class
"""
import logging
import os

from .joint import Joint
from .hardware import Hardware
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
        self.z_hw = Hardware()
        self.z = Joint(#odrv_serial_num=joints["z"]["odrv_serial_num"],
                       #axis_name=joints["z"]["axis_name"],
                       hardware=self.z_hw,
                       name=joints["z"]["name"],
                       config_file=config_file
                       )
        self.codo_hw = Hardware()
        self.codo = Joint(#odrv_serial_num=joints["codo"]["odrv_serial_num"],
                          #axis_name=joints["codo"]["axis_name"],
                          hardware=self.codo_hw,
                          name=joints["codo"]["name"],
                          #enable_odrv=False, # TODO FIX by creating a singleton for odrv init
                          config_file=config_file,
                          #odrv=self.z.odrv
                          )
        self.hombro_hw = Hardware()
        self.hombro = Joint(#odrv_serial_num=joints["hombro"]["odrv_serial_num"],
                            #axis_name=joints["hombro"]["axis_name"],
                            hardware=self.hombro_hw,
                            name=joints["hombro"]["name"],
                            config_file=config_file)
        self.a_hw = Hardware()
        self.a = Joint(hardware=self.a_hw,
                       name="a")
        # dict with all joints
        self.all_joints = {"hombro": self.hombro,
                           "codo": self.codo,
                           "z": self.z,
                           "a": self.a
                           }
        # dict with all home position per joint (joint's zero, not cartesian)
        self.all_pos_0 = {"hombro": self.hombro.pos_0,
                          "codo": self.codo.pos_0,
                          "z": self.z.pos_0,
                          "a": 0
                          }
        self.h_len = dimensions["humero_len"]
        self.rc_len = dimensions["radio_cubito_len"]
        self.max_hombro_degree = dimensions["max_hombro_degree"]
        self.max_codo_degree = dimensions["max_codo_degree"]
        self.cartesian_0 = dimensions["cartesian_0"]
        self.orientation = dimensions["orientation"]
        self.is_initialized = True
        self.is_setted_up = False

    def setup(self):
        """
        Setup all joints
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logger.info("Setup routine")
        #for joint in self.all_joints.values():
        for joint in reversed(self.all_joints.values()):
            joint.joint_setup()
        self.is_setted_up = True

    def go_home(self):
        """
        Homing routine
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logger.info("Doing homing routine")
        self.move2(x=self.cartesian_0["x"],
                   y=self.cartesian_0["y"],
                   z=self.cartesian_0["z"])

    def move2(self,
            x: float,
            y: float,
            z: float,
            a: float = 0,
            mode: str = None):
        """
        Move to cartesian target position

        Parameters
        ----------
        x : float
            x position
        y : float 
            z position
        z : float
            z position
        a : float
            a position
        mode : str 
            to use an specific mode (not implemented yet)

        Returns
        -------
        None
        """
        logger.info("Moving to position x: %.2f, y: %.2f, z: %.2f in %s mode",
                    x,
                    y,
                    z,
                    a,
                    mode)
        # given x,y position calculate hombro and codo angles using
        # inverse kinametic
        angles = inverse_kinematic(x=x,
                                   y=y,
                                   h_len=self.h_len,
                                   rc_len=self.rc_len,
                                   max_hombro_degree=self.max_hombro_degree,
                                   max_codo_degree=self.max_codo_degree,
                                   orientation=self.orientation
                                   )
        all_pos = {"hombro": angles["hombro"],
                   "codo": angles["codo"],
                   "z": z,
                   "a": a}
        for joint_name, joint in self.all_joints.items():
            pos_from_0 = all_pos[joint_name] - self.all_pos_0[joint_name]
            joint.joint_move2(position_increment=pos_from_0,
                          from_goal_point=False)
