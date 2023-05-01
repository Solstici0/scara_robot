"""
joint.py:
    SCARA joint class
"""
import logging
import odrive
import os

from .tools.hardware_layer import pos2motors
from .tools.manage_files import load_robot_config

logger = logging.getLogger(__name__)

class Joint():
    """
    Joint class
    """
    def __init__(self,
               odrv_serial_num: str,
               axis: str,
               name: str = None,
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
        #TODO axis should be an odrv.axis object or a fake one
        self.odrv_serial_num = odrv_serial_num
        self.axis = axis
        self.name = name
        self.pos_0 = None
        self.hardware_correction = None
        # allow fake odrive for testing
        if self.odrv_serial_num is not None:
            self.odrv = odrive.find_any(serial_number=self.odrv_serial_num)
        else:
            import tools.fake_odrive as fake_odrive
            self.odrv = fake_odrive.find_any()
            self.pos_0 = 0
            self.hardware_correction = 0
        self.joint = getattr(self.odrv, self.axis)()
        # load information if joint is defined in the config file
        if self.name in [joints.keys()]:
            self.pos_0 = joints[self.name]["pos_0"]
            self.hardware_correction = joints[self.name]["hardware_corrections"]
        self.state = self.joint.current_state
        logger.info("Axis %s instantiated as %s", self.axis, self.name)

    def j_setup(self):
        """
        """
        logger.info("Setup routine for %s axis", self.axis)
        while self.state == 1:
            self.joint.requested_state = 7
            #sleep 12
            self.joint.requested_state = 11
            #sleep 15
            #if self.odrv_serial_num is None:
            #    self.joint.requested_state = 2
            self.state = self.joint.current_state
            if self.state == 1:
                logger.info("%s axis successfully what?")
                self.joint.resquested_state = 8
                self.state = self.joint.current_state
                if self.state == 8:
                    logger.info("%s axis successfully enters control mode",
                                self.name)
            else:
                logger.info("Homing failed. %s axis current state %i",
                            self.name, self.joint.current_state)
                if self.odrv_serial_num is not None:
                    dump_errors(self.odrv, True)
                #sleep 1

    def j_go_home(self):
        """
        """
        logger.info("Axis %s going to home position", self.axis)

    def j_move2(self, position):
        """
        """
        logger.info("Axis %s going to %.2f position",
                    self.axis, position_increment)
        position_inc_corrected = pos2motors(
                        joint_position=position_increment,
                        hardware_correction=self.hardware_correction)
        self.joint.controller.move_incremental(pos_increment=position_inc_corrected,
                                               from_goal_point=from_goal_point)
