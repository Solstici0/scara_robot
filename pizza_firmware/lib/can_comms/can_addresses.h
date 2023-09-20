#define CAN_BUS_SPEED 500E3
#define CAN_SELF_ID 0x694

enum PIZZA_ACTUATORS{
    STEPPER,
    SERVO,
    DIGITAL_OUTPUT,
};

enum PIZZA_FUNCTIONS{
    ENABLE,
    STATE = 0,
    SPEED,
    ACCELERATION,
    MOVE,


};
//      bit number        76543210
//                        ||||||||
#define IS_WRITING_MASK 0b10000000
#define ACTUATOR_MASK   0b01110000
#define FUNCTION_MASK   0b00001111
