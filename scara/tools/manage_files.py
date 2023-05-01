"""
manage_files.py
    some general tools for manage files and config files
"""
import os
import yaml

def load_robot_config(path: str):
    """
    Load robot config file.
    Paramters:
    ----------
    path : path to file.
    Retunrs:
    --------
    joints : dictionary with each joint information
    dimensions : dictionary with dimensions information
    """
    with open(path) as f:
        services = yaml.safe_load(f)
    return services["joints"], \
            services["dimensions"]
