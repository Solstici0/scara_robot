"""
joint.py:
    SCARA joint class
"""
import logging
import odrive
import os
import time

#from .tools.communication
from .tools.hardware_layer import pos2motors
from .tools.manage_files import load_robot_config
from .tools.fake_odrive import find_any

logger = logging.getLogger(__name__)

class Joint():
    """
    Joint class
    """
    def __init__(self,
               odrv_serial_num: str,
               axis: str,
               name: str = None,
               enable_odrv: bool = True,
               config_file: str = None):
        if config_file is not None:
            self.config_file = config_file + ".yaml"
            abs_path = os.path.dirname(__file__)
            self.config_path = os.path.join(abs_path,
                                            "config",
                                            self.config_file)
            # load configuration
            joints, _ = load_robot_config(self.config_path)
        else:
            joints = {}
        # TODO axis should be an odrv.axis object or a fake one
        self.odrv_serial_num = odrv_serial_num
        # TODO axis should be axis_name and joint should be axis
        self.axis = axis
        self.name = name
        self.pos_0 = None
        self.hardware_correction = joints[self.name]["hardware_correction"]
        # allow fake odrive for testing
        if (self.odrv_serial_num is not None and
            enable_odrv):
            self.odrv = odrive.find_any(serial_number=self.odrv_serial_num)
            logger.info("Enable odrive %s for %s joint",
                        self.odrv_serial_num, self.name)
            #self.odrv = cm.get_hardware(hardware_type=,
            #                            serial_number=self.odrv_serial_num)
        else:
            #self.odrv = fake_odrive.find_any()
            self.odrv = find_any()
            self.pos_0 = 0
            self.hardware_correction = 0
        self.joint = getattr(self.odrv, self.axis)
        # load information if joint is defined in the config file
        if self.name in [joints.keys()]:
            self.pos_0 = joints[self.name]["pos_0"]
            self.hardware_correction = joints[self.name]["hardware_corrections"]
        #self.state = self.joint.current_state
        self.state = getattr(self.joint,
                             "current_state")
        logger.info("Axis %s instantiated as %s", self.axis, self.name)

    def j_setup(self):
        """
        Setup routine for joints
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logger.info("Setup routine for %s axis", self.axis)
        while self.state == 1:
            self.joint.requested_state = 7
            time.sleep(12)
            self.joint.requested_state = 11
            time.sleep(15)
            #if self.odrv_serial_num is None:
            #    self.joint.requested_state = 2
            self.state = self.joint.current_state
            if self.state == 1:
                logger.info("%s axis successfully what?")
                self.joint.requested_state = 8
                self.state = self.joint.current_state
                if self.state == 8:
                    logger.info("%s axis successfully enters control mode",
                                self.name)
            else:
                logger.info("Homing failed. %s axis current state %i",
                            self.name, self.joint.current_state)
                if self.odrv_serial_num is not None:
                    dump_errors(self.odrv, True)
                time.sleep(1)

    def j_go_home(self):
        """
        Homing routine for joints
        
        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        logger.info("Axis %s going to home position", self.axis)
        self.j_move2(self.pos_0)

    def j_move2(self, position_increment: float, from_goal_point: bool =False):
        """
        Move joint to target position

        Parameters
        ----------
        position_increment : float
            incremental position from current position
        from_goal_point : bool

        Returns
        -------
        None
        """
        logger.info("Axis %s going to %.2f position",
                    self.axis, position_increment)
        position_inc_corrected = pos2motors(
                        joint_position=position_increment,
                        hardware_correction=self.hardware_correction)
        self.joint.controller.move_incremental(pos_increment=position_inc_corrected,
                                               from_goal_point=from_goal_point)

    def dump_errors(self):
        """
        Recicle dump errors from odrive
        """
        odrive.dump_errors(self.odrv)
