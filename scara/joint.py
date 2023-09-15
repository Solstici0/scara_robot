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
import scara.tools.exceptions as exceptions
from scara.tools.enums_dict import *

logger = logging.getLogger(__name__)

class Joint():
    """
    Joint class
    """
    def __init__(self,
               odrv_serial_num: str,
               axis_name: str,
               name: str = None,
               enable_odrv: bool = True,
               config_file: str = None,
               odrv = None):
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
        self.axis_name = axis_name
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
        elif (enable_odrv is not None and 
                odrv is not None):
            self.odrv = odrv
            logger.info("Enable odrive %s for %s joint",
                        self.odrv_serial_num, self.name)
        elif self.odrv_serial_num is None:
            #self.odrv = fake_odrive.find_any()
            self.odrv = find_any()
            self.pos_0 = 0
            self.hardware_correction = 0
        else:
            pass
        self.axis = getattr(self.odrv, self.axis_name)
        # load information if joint is defined in the config file
        if self.name in joints.keys():
            self.pos_0 = joints[self.name]["pos_0"]
            self.hardware_correction = joints[self.name]["hardware_correction"]
            logger.debug("Joint %s in joints.keys()", self.name)
        else:
            logger.debug("Joint %s NOT in joints.keys()", self.name)
        #self.state = self.axis.current_state
        self.state = getattr(self.axis,
                             "current_state")
        logger.info("Axis %s instantiated as %s", self.axis_name, self.name)

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
        logger.info("Setup routine for %s axis", self.axis_name)
        # FIX: improve rutine below including 
        # logic for retry

        self.axis.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
        time.sleep(0.2)
        exceptions.raise_except(self.axis,AXIS_STATE_ENCODER_OFFSET_CALIBRATION) #exception if unable to enter requested state
        exceptions.timeout_except(self.axis,AXIS_STATE_ENCODER_OFFSET_CALIBRATION) #exception if time out and still in the same state
        logger.info('succesfully entered AXIS_STATE_ENCODER_OFFSET_CALIBRATION')  
        
        #execute homing
        self.axis.requested_state = AXIS_STATE_HOMING 
        time.sleep(0.2)
        exceptions.raise_except(self.axis,AXIS_STATE_HOMING) #exception if unable to enter requested state
        exceptions.timeout_except(self.axis,AXIS_STATE_HOMING)  #exception if time out and still in the same state
        logger.info('Current axis successfully homed')
        
        #execute control loop
        self.axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        time.sleep(0.2)
        exceptions.raise_except(self.axis, AXIS_STATE_CLOSED_LOOP_CONTROL) #exception if unable to enter requested state
        logger.info('Current axis successfully enters control mod3')

        
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
        logger.info("Axis %s going to home position", self.axis_name)
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
                    self.axis_name, position_increment)
        position_inc_corrected = pos2motors(
                        joint_position=position_increment,
                        hardware_correction=self.hardware_correction)
        self.axis.controller.move_incremental(position_inc_corrected,
                                                from_goal_point)
    
    def j_move_abs(self,new_target : float):
        """
        Updates the target position of the odrive controller, this results
        in an absolute movement in turns.

        parameters:
        -----------
        -new_target (float): new target for the controller, in turns respect
        of the 0 position

        returns:
        --------
        -int : the state of the function, 0 if succesfull
        """
        self.axis.controller.input_pos = new_target
        return 0

    # include property
    def dump_errors(self):
        """
        Recicle dump errors from odrive
        """
        odrive.utils.dump_errors(self.odrv)
