import logging
import numpy as np

#from .config import config

logger = logging.getLogger(__name__)

def inverse_kinematic(x: float,
                    y: float,
                    h_len: float = 330.15,
                    rc_len: float = 338.0,
                    max_hombro_degree: float = 90.0/180*np.pi,
                    max_codo_degree: float = 135.0/180*np.pi,
                    orientation = 'left') -> dict:
    """
    Calculate inverse kinematic of the arm

    Parameters:
    -----------
    x : x target position
    y : y target position
    h_len : humero length
    rc_len : radio-cubito length

    Returns:
    --------
    angles : hombro and codo angles
    angle["hombro"]
    angle["codo"]
    """
    if orientation not in ["right", "left"]:
        logger.error("orientation mode error. orientation",
                    "should be equal to 'right' or 'left'")
        raise ValueError("orientation mode error. orientation",
                        "should be equal to 'right' or 'left'")

    logger.info("x target position %.2f", x)
    logger.info("y target position %2.f", y)

    cos_hombro_angle = min(max((x**2 + y**2 - h_len**2 - rc_len**2)
                               /(2 * h_len * rc_len),-1),1)
    logger.debug("cos_hombro_angle %.2f", cos_hombro_angle)
    if orientation == "left":
        codo_angle = np.arctan(np.sqrt(1 - cos_hombro_angle**2)/ \
                               cos_hombro_angle)
        if x == 0:
            hombro_angle = np.sign(y) * np.pi / 2.0 - \
                      np.arctan(rc_len * np.sin(codo_angle) / \
                      (h_len + rc_len * np.cos(codo_angle)))
        else:
            hombro_angle = np.arctan(y/x) - \
                           np.arctan(rc_len * np.sin(codo_angle) / \
                                     (h_len + rc_len * np.cos(codo_angle)))
    else:
        codo_angle = np.arctan(-np.sqrt(1 - cos_hombro_angle**2) / \
                            cos_hombro_angle)
        if x == 0:
            hombro_angle = np.sign(y) *np.pi / 2.0 + \
                           np.arctan(rc_len * np.sin(codo_angle) / \
                                     (h_len + rc_len * np.cos(codo_angle)))
        else:
            hombro_angle = np.arctan(y / x) + \
                      np.arctan(rc_len * np.sin(codo_angle) / \
                                (h_len + rc_len * np.cos(codo_angle)))

    logger.info("hombro_angle: %.2f", hombro_angle)
    logger.info("codo_angle: %.2f", codo_angle)

    # handle angles out of range
    if np.abs(hombro_angle) > max_hombro_degree:
        logger.warning("hombro_angle out of range! hombro_angle: %.2f",
                        hombro_angle)
    elif np.abs(codo_angle) > max_codo_degree:
        logger.warning("codo_angle out of range! codo_angle: %.2f",
                        codo_angle)

    if ((np.abs(hombro_angle) < max_hombro_degree) and
        (np.abs(codo_angle) < max_codo_degree)):
        angles = {}
        angles["hombro"] = hombro_angle
        angles["codo"] = codo_angle
        return angles
