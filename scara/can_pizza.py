import can

CAN_BUS_SPEED = 500E3
CAN_SELF_ID = 0x694
CAN_RASPI_ID = 0x420


PIZZA_ACTUATORS = {'STEPPER' : 0,
                   'SERVO' : 1,
                   'DIGITAL_OUTPUT' : 2}

PIZZA_FUNCTIONS  = {'ENABLE' : 0,
                    'STATE' : 0,
                    'SPEED' : 1,
                    'ACCELERATION' :2 ,
                    'MOVE' : 3}

