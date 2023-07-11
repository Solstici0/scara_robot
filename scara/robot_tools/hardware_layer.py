import logging

#from .config import config

logger = logging.getLogger(__name__)

def pos2motors(joint_position: float, hardware_correction: float = 0) -> float:
    """
    Takes into account gears and transform position to
    motor turns units

    Parameters:
    -----------
    joint_name
    joint_position: target position before proper transformation

    Returns:
    --------
    motor_turns: position in motor turns units

    """
    motor_turns = joint_position * hardware_correction
    logger.debug("motor turns for joint: %.2f", motor_turns)
    return motor_turns
