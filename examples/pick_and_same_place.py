import scara
import logging 
import scara.can_pizza as pizza

point = [0.0,400.0,0.0]

command_sole0OFF = {'IS_WRITING':1,
                   'ACTUATOR': pizza.PIZZA_ACTUATORS['DIGITAL_OUTPUT'],
                   'FUNCTION':pizza.PIZZA_FUNCTIONS['ENABLE'],
                   'ACTUATOR_NUM' :0,
                   'PARAM' : 0}

command_sole0ON = {'IS_WRITING':1,
                   'ACTUATOR': pizza.PIZZA_ACTUATORS['DIGITAL_OUTPUT'],
                   'FUNCTION':pizza.PIZZA_FUNCTIONS['ENABLE'],
                   'ACTUATOR_NUM' :0,
                   'PARAM' : 1}


scara.logger.setLevel(logging.INFO)
nelen = scara.Robot()


if __name__ == '__main__':
    while True:
        input()
        nelen.move(point[0], point[1], 180.0,'right')
        input()
        nelen.move(point[0], point[1], 0.0,'right')
        input()
        pizza.write(command_sole0ON)
        input()
        nelen.move(point[0], point[1], 180.0,'right')
        input()
        nelen.move(point[0], point[1], 180.0,'left')
        input()
        nelen.move(point[0], point[1], 0.0,'left')
        input()
        pizza.write(command_sole0OFF)
        