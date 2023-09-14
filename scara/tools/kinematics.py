"""
This files implements the direct and inverse kinematics of an scara robot,
the coordinate system is as follows, 
1.-The origin's x and y copordinates are in the first joint location. Z is
   the uppermost position of the final actuator.
2.-when both of the revolute joints are in the half of their motion range the
   scara is lying in the y axis and the x axis increases to the right (looking from
   the origin with the arm to the front)
"""
import numpy as np
import math
import scara.tools.manage_files as mng

joints, dimensions = mng.load_robot_config('scara/config/default.yaml')


red_ratio=7
r1=dimensions["humero_len"]
r2=dimensions["radio_cubito_len"]
maxtheta1=[0, 2*dimensions["max_hombro_degree"]]
maxtheta2=[-1*dimensions["max_codo_degree"],dimensions["max_codo_degree"]]
maxr = (r1+r2)**2

tolerance = 1e-12
def direct_kin(theta1,theta2):
    theX=r1*math.cos(theta1)+r2*math.cos(theta2+theta1)
    theY=r1*math.sin(theta1)+r2*math.sin(theta2+theta1)
    return [theX,theY]

def check_angle(angle,limits):
    if angle < limits[0]:
        if limits[0]-angle < tolerance:
            return limits[0]
        new_angle = angle + 2*math.pi
        if limits[0] <= new_angle <= limits[1]:
            return new_angle
        elif limits[1] - new_angle <= tolerance:
            return limits[1]
        else:
            #in this case the point is not achievable
            return None
    elif angle > limits[1]:
        if angle-limits[1] < tolerance:
            return limits[1]
        new_angle = angle - 2*math.pi
        if limits[0] <= new_angle <= limits[1]:
            return new_angle
        else:
            #in this case the point is not achievable
            return None
    else:
        return angle

def inverse_kin(x,y,ori="right"):
    rcuadrado=x**2+y**2
    if rcuadrado == maxr:
        return {"hombro":math.atan2(y,x),
                "codo":0}
    
    B=(rcuadrado-r1**2-r2**2)/(2*r1*r2)
    theta2=math.atan2(math.sqrt(1-B*B),B)
    if (ori=="right"):
        theta1=math.atan2(y,x)-math.atan2(r2*math.sin(theta2),(r1+r2*math.cos(theta2)))
    elif (ori=="left"):
        theta2=2*math.pi-theta2
        theta1=math.atan2(y,x)-math.atan2(r2*math.sin(theta2),(r1+r2*math.cos(theta2)))
    
    theta1 = check_angle(theta1,maxtheta1)
    theta2 = check_angle(theta2,maxtheta2)
    return {"hombro":theta1,
            "codo":theta2}

