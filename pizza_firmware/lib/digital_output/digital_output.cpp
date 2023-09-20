#include <Arduino.h>

namespace digital_outputs
{
    const int DIGITAL_OUTPUT_PIN_0 = 5; //!< arduino numbering for the DO0 pin
    const int DIGITAL_OUTPUT_PIN_1 = 6; //!< arduino numbering for the DO1 pin
    
    const int DO_ARRAY[]={DIGITAL_OUTPUT_PIN_0,
                          DIGITAL_OUTPUT_PIN_1};
    void setup(){
        /*! digital output pins configured as outputs
        */
        for (int do_num=0;do_num<2;do_num++){
            pinMode(DO_ARRAY[do_num],OUTPUT);
        }
    }

    int state(boolean is_writing, int do_num, boolean value){
        /*! Read or set state of the digital output
        *  
        *  @param is_writing false to read the state, true to change it
        *  @param do_num number of digital_output read or set the state
        *  @param value True to turn on and false to turn off
        *  @return 0 if is_writing is set to true or the state of the digital output state in the contrary
        */
        if (is_writing){
            if (value){
                digitalWrite(DO_ARRAY[do_num],HIGH);
            }
            else{
                digitalWrite(DO_ARRAY[do_num],LOW);
            }
            return 0;
        }
        else{
           //is reading
           return digitalRead(DO_ARRAY[do_num]);
        }
    }
}