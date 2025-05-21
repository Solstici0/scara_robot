from odrive_can.src.axis import Axis
import logging
import os
from tools.manage_files import load_robot_config
import scara.odrive_can.src.odrive_enums as enums
import time
import tools.exceptions as exceptions

logger = logging.getLogger(__name__)

OFFSET_CALIB_TIME = 10
HOMING_TIME = 10

class Joint_can():
    def __init__(self,
                 axis_name: str,
                 config_file: str = None):
        if config_file:
            self.config_file = config_file + ".yaml"
            abs_path = os.path.dirname(__file__)
            self.config_path = os.path.join(abs_path,
                                            "config",
                                            self.config_file)
            # load configuration
            joints, _ = load_robot_config(self.config_path)
            if not ('axis_can_id' in joints[axis_name].keys()):
                raise Exception('Configuration files does not have a can_id for %s axis', axis_name)
            self.axis_can = Axis(joints[axis_name],"vcan0")
            self.axis_name = axis_name
        else:
            raise Exception('No configuration file was given')
        pass
    def j_setup(self,startup_position = None):
        logger.info("Setup routine for %s axis", self.axis_name)

        self.axis_can.set_requested_state(enums.AxisState(enums.AXIS_STATE_ENCODER_OFFSET_CALIBRATION))
        time.sleep(0.2)
        self.wait_for_state(enums.AxisState(enums.AXIS_STATE_ENCODER_OFFSET_CALIBRATION),
                            OFFSET_CALIB_TIME)
        logger.info('succesfully entered AXIS_STATE_ENCODER_OFFSET_CALIBRATION')
        self.wait_for_state(enums.AxisState(enums.AXIS_STATE_IDLE),
                            OFFSET_CALIB_TIME) #exception if time out and still in the same state
        logger.info('got out of AXIS_STATE_ENCODER_OFFSET_CALIBRATION')
        #execute homing
        self.axis_can.set_requested_state(enums.AxisState(enums.AXIS_STATE_HOMING))
        time.sleep(0.2)
        self.wait_for_state(enums.AxisState(enums.AXIS_STATE_HOMING),
                            HOMING_TIME) #exception if unable to enter requested state
        logger.info('succesfully entered AXIS_STATE_HOMING')  
        self.wait_for_state(enums.AxisState(enums.AXIS_STATE_IDLE),
                            HOMING_TIME) #exception if time out and still in the same state
        logger.info('Current axis successfully homed')
        #execute control loop
        self.axis_can.set_requested_state(enums.AxisState(enums.AXIS_STATE_CLOSED_LOOP_CONTROL))
        time.sleep(0.2)
        self.wait_for_state(enums.AxisState(enums.AXIS_STATE_CLOSED_LOOP_CONTROL)) #exception if unable to enter requested state
        logger.info('Current axis successfully enters control mod3')
        if startup_position:
            self.j_move_abs(startup_position)
        pass

    def j_go_home(self):
        logger.error('unimplemented')
        pass

    def j_move2(self, position_increment: float, from_goal_point: bool =False):
        logger.error('unimplemented')
        pass

    def j_move_abs(self,new_target : float):
        logger.info("%s axis setpoint will change to %f",self.name,new_target)
        self.axis_can.set_input_pos(new_target)

    def dump_errors(self,argument = None):
        errors = self.axis_can.dump_errors(argument)
        if (errors['MOTOR_ERROR'] != enums.MotorError(enums.MOTOR_ERROR_NONE) or
            errors['ENCODER_ERROR'] != enums.EncoderError(enums.ENCODER_ERROR_NONE) or
            errors['CONTROLLER_ERROR'] != enums.ControllerError(enums.CONTROLLER_ERROR_NONE)):
            logger.info('dumping errors for %s \n%s',self.axis_name,errors)
        else:
            logger.error('dumping errors for %s \n%s',self.axis_name,errors)

    def wait_for_state(self, expected_state:enums.AxisState, timeout=None)->bool:
        if timeout:
            exceptions.general_eval_except(
                lambda : self.axis_can.get_current_state() == expected_state,
                timeout)
        else:
            exceptions.general_eval_except(
                lambda : self.axis_can.get_current_state() == expected_state)
