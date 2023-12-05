"""
robot.py:
    SCARA robot class
"""
import logging
import os

from .joint import Joint
from .tools.inverse_kinematic import inverse_kinematic
import scara.can_pizza as pizza
from .tools.manage_files import load_robot_config
import scara.tools.kinematics as kin
logger = logging.getLogger(__name__)
import pickle as pkl
import time
from pathlib import Path

home_path = Path('~').expanduser()
data_path = home_path / 'data' / 'last_data.pkl'

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
        self.z = Joint(odrv_serial_num=joints["z"]["odrv_serial_num"],
                       axis_name=joints["z"]["axis_name"],
                       name=joints["z"]["name"],
                       config_file=config_file
                       )
        self.codo = Joint(odrv_serial_num=joints["codo"]["odrv_serial_num"],
                          axis_name=joints["codo"]["axis_name"],
                          name=joints["codo"]["name"],
                          enable_odrv=False, # TODO FIX by creating a singleton for odrv init
                          config_file=config_file,
                          odrv=self.z.odrv)
        self.hombro = Joint(odrv_serial_num=joints["hombro"]["odrv_serial_num"],
                            axis_name=joints["hombro"]["axis_name"],
                            name=joints["hombro"]["name"],
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
            if joint.pos_0_in_turns:
                joint.j_setup(joint.pos_0_in_turns)
            else:
                joint.j_setup()
        pizza.motor_enable(1)

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
        all_pos = {"hombro": angles["hombro"], "codo": angles["codo"], "z": z}
        for joint_name, joint in self.all_joints.items():
            pos_from_0 = all_pos[joint_name] - self.all_pos_0[joint_name]
            joint.j_move2(position_increment=pos_from_0,
                          from_goal_point=False)
    def move(self,
             x: float,
             y: float,
             z: float,
             orientation : str = "right"):
        """
        Moves the robot to the desired position in cartesians.
        
        """
        new_radians = kin.inverse_kin(x,y,orientation)
        new_turns = {"hombro" : new_radians["hombro"]*self.hombro.hardware_correction,
                     "codo": new_radians["codo"]*self.codo.hardware_correction,
                     "z": z*self.z.hardware_correction}
        self.hombro.j_move_abs(new_turns["hombro"])
        self.codo.j_move_abs(new_turns["codo"])
        self.z.j_move_abs(new_turns["z"])
    
    def move_with_data(self,
             x: float,
             y: float,
             z: float,
             orientation : str = "right",
             frequency = 100):
        """
        Moves the robot to the desired position in cartesians. It also stores the data in a pickle file
        """
        period_in_ns = int(1e9/frequency)
        data = []
        new_radians = kin.inverse_kin(x,y,orientation)
        new_turns = {"hombro" : new_radians["hombro"]*self.hombro.hardware_correction,
                     "codo": new_radians["codo"]*self.codo.hardware_correction,
                     "z": z*self.z.hardware_correction}
        self.hombro.j_move_abs(new_turns["hombro"])
        self.codo.j_move_abs(new_turns["codo"])
        self.z.j_move_abs(new_turns["z"])
        timer = time.time_ns()-period_in_ns
        while True:
            if time.time_ns()-timer >= period_in_ns:
                timer = time.time_ns()
                new_data= [timer,
                                self.hombro.axis.controller.pos_setpoint,
                                self.hombro.axis.encoder.pos_estimate,
                                self.hombro.axis.controller.vel_setpoint,
                                self.hombro.axis.encoder.vel_estimate,
                                self.hombro.axis.motor.current_control.Iq_setpoint,
                                self.hombro.axis.motor.current_control.Iq_measured,
                                self.codo.axis.controller.pos_setpoint,
                                self.codo.axis.encoder.pos_estimate,
                                self.codo.axis.controller.vel_setpoint,
                                self.codo.axis.encoder.vel_estimate,
                                self.codo.axis.motor.current_control.Iq_setpoint,
                                self.codo.axis.motor.current_control.Iq_measured]
                data.append(new_data)
            if self.hombro.axis.controller.trajectory_done \
               and self.codo.axis.controller.trajectory_done \
               and self.z.axis.controller.trajectory_done:
                break
            elif self.hombro.odrv.error != 0 and self.z.odrv.error != 0:
                break
        with open(data_path,'rb') as file:
            pkl.dump(data,file)
            
    


    def move_direct(self, turns_hombro, turns_codo):
        self.hombro.axis.controller.input_pos = (turns_hombro)
        self.codo.axis.controller.input_pos = (turns_codo)

    def a_move(self,steps):
        return pizza.move_stepper(steps)
    
    def solenoid(self,state):
        return pizza.solenoid(state)
        
