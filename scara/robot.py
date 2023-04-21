"""
scara.py:
    SCARA robot class
"""
import logging 

logger = logging.getLogger(__name__)

class Scara():
    """
    Scara class
    """
    def __init__(self):
        logger.info('Initializing SCARA robot')
        logger.warning('Initializing SCARA robot, warning')
        print('hola!')
        #pass

if __name__ == '__main__':
    nelen = Scara()
