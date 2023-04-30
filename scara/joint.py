"""
joint.py:
    SCARA joint class
"""
import logging

logger = logging.getLogger(__name__)

class Joint():
    """
    Joint class
    """
    def __init__(self,
               axis: str = '0'):
        #TODO axis should be an odrv.axis object or a fake one
        self.axis = axis
        logger.info("Axis %s instantiated", self.axis)

    def j_setup(self):
        """
        """
        logger.info("Setup routine for %s axis", self.axis)

    def j_go_home(self):
        """
        """
        logger.info("Axis %s going to home position", self.axis)

    def j_move2(self, position):
        """
        """
        logger.info("Axis %s going to %.2f position", self.axis, position)
