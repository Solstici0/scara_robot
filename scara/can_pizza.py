import can
import logging
import ctypes

logger = logging.getLogger(__name__)

PIZZA_TIMEOUT = 2

CAN_BUS_SPEED = 250E3
CAN_PIZZA_ID = 0x1A4
CAN_RASPI_ID = 0x45


IS_WRITING_SHIFT = 7
ACTUATOR_SHIFT = 4
FUNCTION_SHIFT = 0

PIZZA_ACTUATORS = {'STEPPER' : 0,
                   'SERVO' : 1,
                   'DIGITAL_OUTPUT' : 2}

PIZZA_FUNCTIONS  = {'ENABLE' : 0,
                    'STATE' : 0,
                    'SPEED' : 1,
                    'ACCELERATION' :2 ,
                    'MOVE' : 3}
INIT_ACCEL = 10
INIT_SPEED = 100

def write(command:dict):
    is_writing = command['IS_WRITING']
    actuator = command['ACTUATOR']
    function = command['FUNCTION']
    actuator_num = command['ACTUATOR_NUM']
    param  = command['PARAM']
    can_data = [0,0,0,0,0,0,0,0]
    can_data[0] = (is_writing<<IS_WRITING_SHIFT) \
                  +(actuator<<ACTUATOR_SHIFT) \
                  +(function<<FUNCTION_SHIFT)
    can_data[1] = actuator_num
    can_data[2] = param & 0xff
    can_data[3] = param >> 8
    filter =[{"can_id": CAN_RASPI_ID, "can_mask": 0x7FF, "extended": False},]

    with can.Bus(interface='socketcan', 
                 channel='can0',
                 bitrate=CAN_BUS_SPEED,
                 can_filters = filter ) as bus:

        msg = can.Message(
            arbitration_id=CAN_PIZZA_ID,
            data=can_data,
            is_extended_id=False
        )
        try:

            bus.send(msg)

            print(f"Message sent on {bus.channel_info}")
            answer = bus.recv(timeout = PIZZA_TIMEOUT)
            return answer.data[0]+(answer.data[1]<<8)
        except can.CanError:
            print("Message NOT sent")


def acceleration(mot_number, new_acc=None):
    if new_acc:
        is_writing = 1
    else:
        is_writing = 0
        new_acc = 0
        
    msg = {'IS_WRITING': is_writing,
            'ACTUATOR': PIZZA_ACTUATORS['STEPPER'],
            'FUNCTION': PIZZA_FUNCTIONS['ACCELERATION'],
            'ACTUATOR_NUM':mot_number,
            'PARAM':new_acc}

    return write(msg)

def speed(mot_number, new_speed=None):
    if new_speed:
        is_writing = 1
    else:
        is_writing = 0
        new_speed = 0
        
    msg = {'IS_WRITING': is_writing,
            'ACTUATOR': PIZZA_ACTUATORS['STEPPER'],
            'FUNCTION': PIZZA_FUNCTIONS['SPEED'],
            'ACTUATOR_NUM':mot_number,
            'PARAM':new_speed}
    return write(msg)

def solenoid(new_state=None):
    if new_state:
        is_writing = 1
    else:
        is_writing = 0
        new_state = 0
    msg = {'IS_WRITING': is_writing,
            'ACTUATOR': PIZZA_ACTUATORS['DIGITAL_OUTPUT'],
            'FUNCTION': PIZZA_FUNCTIONS['STATE'],
            'ACTUATOR_NUM':0,
            'PARAM':new_state}
    return write(msg)


def move_stepper(mot_num : int, steps: int=None):
    if steps:
        is_writing = 1
        steps = to_raw_byte(steps)
    else:
        is_writing = 0
        steps = 0
    msg = {'IS_WRITING': is_writing,
            'ACTUATOR': PIZZA_ACTUATORS['STEPPER'],
            'FUNCTION': PIZZA_FUNCTIONS['MOVE'],
            'ACTUATOR_NUM':mot_num,
            'PARAM':steps}
    return write(msg)

def to_raw_byte(input_int):
    if 0 <= input_int <= 32767:
        return input_int
    elif -32768 <= input_int < 0:
        return 0x8000+ (32768+input_int)
    else:
        return 0
