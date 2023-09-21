"""
WARNING : this script should only work if the machine is already initialized
and if there is no other terminal with an initialized object of the scara robot
"""
import logging
import time

import scara

scara.logger.setLevel(logging.INFO)
nelen = scara.Robot()

# do <n_squares>
n_squares = 5
# vertex defines each vertex of the square
# vertex = [x_position, y_position, z_position]
vertex_1 = [-100, 400, 100]
vertex_2 = [-100, 500, 50]
vertex_3 = [100, 500, 150]
vertex_4 = [100, 400, 50]
all_vertex = [vertex_1, vertex_2, vertex_3, vertex_4]
def square_movement():
    for square_num in range(n_squares):
        for vertex in all_vertex:
            nelen.move(vertex[0], vertex[1], vertex[2])
            input()

if __name__ == '__main__':
    square_movement()
