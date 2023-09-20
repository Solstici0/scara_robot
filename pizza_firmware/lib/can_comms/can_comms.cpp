#include "can_comms.h"
#include "can_addresses.h"
#include <MCP2515.h>
#include "digital_output.h"
#include "stepper_motors.h"

using namespace can;

void can::init(uint16_t address){

    if (!CAN.begin(500E3)) {
        Serial.println("Starting CAN failed!");
        while (1);
    }
    CAN.filter(address);
}

int check_for_messages(){
    return CAN.parsePacket();
}

void decide(uint8_t buffer[], uint8_t size){

    bool is_writing  = buffer[0] & IS_WRITING_MASK;
    uint8_t function = buffer[0] & FUNCTION_MASK;
    uint8_t actuator = buffer[0] & ACTUATOR_MASK;
    
    
    
}

