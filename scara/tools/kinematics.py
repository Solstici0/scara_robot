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
r1=1
r2=0.5
maxtheta1=[0,math.pi]
martheta2=[math.pi/4,7*math.pi/4]

def directKin(theta1,theta2):
    theX=r1*math.cos(theta1)+r2*math.cos(theta2+theta1)
    theY=r1*math.sin(theta1)+r2*math.sin(theta2+theta1)
    return [theX,theY]


def inverseKin(x,y,ori="der"):
    rcuadrado=x**2+y**2
    B=(rcuadrado-r1**2-r2**2)/(2*r1*r2)
    theta2=math.atan2(math.sqrt(1-B*B),B)
    if (ori=="der"):
        theta1=math.atan2(y,x)-math.atan2(r2*math.sin(theta2),(r1+r2*math.cos(theta2)))
    elif (ori=="izq"):
        theta2=2*math.pi-theta2
        theta1=math.atan2(y,x)-math.atan2(r2*math.sin(theta2),(r1+r2*math.cos(theta2)))
    return [theta1,theta2]