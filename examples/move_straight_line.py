import argparse
import logging 
import time
import scara
import scara.trayectory_planning.s_curve_trayectory as s_curve
import scara.tools.kinematics as kin
import pickle as pkl
from pathlib import Path

logger = logging.getLogger(__name__)
file_path = Path('/data_dump/last_straight_line.pkl')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Move the scara to the given position "\
                                     +"in a controlled motion")
    parser.add_argument('x', type=float, help='X coordinate')
    parser.add_argument('y', type=float, help='Y coordinate')
    parser.add_argument('z', type=float, help='Z coordinate')
    parser.add_argument('a', type=float, help='A coordinate')
    parser.add_argument('s', type=float, help='S parameter, the greater the faster')

    args = parser.parse_args()



    # Access the values of the arguments
    x = args.x
    y = args.y
    z = args.z
    a = args.a
    s = args.s

    nelen = scara.Robot()  # creates an instance of the scara robot
    current_codo = nelen.codo.axis.encoder.pos_estimate/nelen.codo.hardware_correction
    current_hombro = nelen.hombro.axis.encoder.pos_estimate/nelen.hombro.hardware_correction
    current_z = nelen.z.axis.encoder.pos_estimate/nelen.hombro.hardware_correction
    current_xy = kin.direct_kin(current_hombro,current_codo)
    current_coordinates = [current_xy[0],current_xy[1], current_z]
    
    speed_limit = 500 #mm/s
    acc_limit = 50 #mm/s²
    jerk_limit = 10 #mm/s³
    frequency = 100 # hertz
    period = 1.0/frequency # seconds
    period_in_ns = period*1e9 #ns

    params = s_curve.TrayectoryParams(frequency,speed_limit,acc_limit,jerk_limit,s)
    trajectory = s_curve.dual_axis_euclidean(current_xy,[x,y],params)

    hombro_commands = [point*nelen.hombro.hardware_correction \
                       for point in trajectory.hombro.position]
    codo_commands = [point*nelen.codo.hardware_correction \
                       for point in trajectory.codo.position]
    executed_position = [[0.0]*len(trajectory.x.position),
                        [0.0]*len(trajectory.x.position)]
    time_of_execution = [0]*len(trajectory.x.position)
    this_time = time.thread_time_ns()
    for i in range(len(trajectory.x.position)):
        while time.thread_time_ns() - this_time < period_in_ns:
            pass
        time_of_execution[i] = time.thread_time_ns()
        nelen.move_direct(hombro_commands[i],
                          codo_commands[i])
        executed_position[0][i] = nelen.hombro.axis.encoder.pos_estimate
        executed_position[1][i] = nelen.codo.axis.encoder.pos_estimate

    corrected_codo =[p/nelen.codo.hardware_correction
                     for p in executed_position[1]]   #from turns to rads

    corrected_hombro =[p/nelen.hombro.hardware_correction
                       for p in executed_position[0]]  #from turns to rads
    executed_xy = [kin.direct_kin(theta1,theta2) 
                   for theta1,theta2 in zip(corrected_hombro,corrected_codo)]
    executed_x, executed_y = zip(*executed_xy)

    executed = {'time' : [t - time_of_execution[0] for t in time_of_execution],
              'hombro' : corrected_hombro,
              'codo' : corrected_codo,
              'x' : executed_x,
              'y' : executed_y}
    expected = {'time' : [period_in_ns*i for i in range(len(trajectory.x.position))],
              'hombro' : trajectory.hombro.position,
              'codo' : trajectory.codo.position,
              'x' : trajectory.x.position,
              'y' : trajectory.y.position}
    result = {'expected':expected,
              'executed':executed}
    with open(file_path,'wb') as file:
        pkl.dump(result,file)

    
