import can
import logging

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

    with can.Bus(interface='socketcan', channel='can0', bitrate=CAN_BUS_SPEED) as bus:
        message_filter = can.Filter(arbitration_id=CAN_RASPI_ID,
                                    extended_id=False,  # Set to True if you are using extended IDs
                                    )
        bus.set_filters([message_filter])
        msg = can.Message(
            arbitration_id=CAN_PIZZA_ID,
            data=can_data,
            is_extended_id=False
        )
        try:

            bus.send(msg)

            print(f"Message sent on {bus.channel_info}")
            answer = bus.recv(timeout = PIZZA_TIMEOUT)
            return answer.data[0]+(answer[1]<<8)
        except can.CanError:
            print("Message NOT sent")


def acceleration():
    return
def speed():
    return

def initialize_pizza():
    return

def move_stepper(mot_num : int, steps: int):
    return

def digital_putput():
    return