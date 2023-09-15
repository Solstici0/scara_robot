#include "can_comms.h"
#include <MCP2515.h>
#include "stepper_motors.cpp"
#include "digital_output.cpp"
#include "can_addresses.h"

using namespace can;

void init(){
    if (!CAN.begin(CAN_BUS_SPEED)) {
        Serial.println("Starting CAN failed!");
        while (1);
    }
}
void decide(uint8_t buffer[], uint8_t size){
    for (int i=0;i<size;i++){
        buffer[i] = CAN.read();
    }
    bool is_writing = buffer[0]&IS_WRITING_MASK;
    uint8_t function = buffer[0] & (IS_WRITING_MASK-1);

    switch (function)
    {
    case MOVE_A:
        int steps = buffer[2]+(buffer[3]<<8);
        steppers::move_function(is_writing,buffer[1],steps);
        break;
    case MOVE_SERVO:
        break;
    case DIGITAL_OUTPUT:

        break;
    default:
        break;
    }
    
    if (buffer[0]==69){
        steppers::move_function(true,0,buffer[1]+buffer[2]<<8);
    }

}
int check_for_messages();
