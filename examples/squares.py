import logging
import time

import scara

scara.logger.setLevel(logging.INFO)
nelen = scara.Robot()

# do <n_squares>
n_squares = 5
# vertex defines each vertex of the square
# vertex = [x_position, y_position, z_position]
#vertex_1 = [500, , 0]
#vertex_2
#vertex_3
#vertex_4
all_vertex = [vertex_1, vertex_2, vertex_3, vertex_4]
for square_num in range(n_squares):
    for vertex in all_vertex:
        scara.move2(vertex[0], vertex[1], vertex[2])
        sleep(2)
