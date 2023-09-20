#include <Arduino.h>
#include <SPI.h>
#include "can_comms.h"
#include "stepper_motors.cpp"
#include "can_addresses.h"
// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  steppers::setup();
  can::init(CAN_SELF_ID);
}

void loop() {
  // put your main code here, to run repeatedly:
  int message_size = can::check_for_messages();
  if (message_size>0){
    can::decide(can::buffer,message_size);
    }
  steppers::run_steppers();
}
