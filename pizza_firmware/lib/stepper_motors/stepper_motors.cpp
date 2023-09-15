#include <AccelStepper.h>

/*! \file steppers.h
 *  \brief Definition of constants, variables and functions for stepper motors in flake feeder
 */

// pins
namespace steppers
{
    const int STEPPER0_DIR_PIN          = 7;  //!< Stepper 0 stepper motor direction pin number.
    const int STEPPER0_STEP_PIN         = 8;  //!< Stepper 0 stepper motor step pulse pin number.
    const int STEPPER0_ENABLE_PIN       = 9;  //!< Stepper 0 stepper motor enable pin number.

    const int STEPPER1_DIR_PIN          = 3;  //!< Stepper 1 stepper motor direction pin number.
    const int STEPPER1_STEP_PIN         = 4;  //!< Stepper 1 stepper motor step pulse pin number.<<<<<<<<    cgggggggggggggggggggggghy
    const int STEPPER1_ENABLE_PIN       = 9;  //!< Stepper 1 stepper motor enable pin number.

    const int STEPPER_PINS[2][3] = {
        {STEPPER0_STEP_PIN, STEPPER0_DIR_PIN, STEPPER0_ENABLE_PIN},
        {STEPPER1_STEP_PIN, STEPPER1_DIR_PIN, STEPPER1_ENABLE_PIN}
        }; 
        //!< Matrix that holds all the pins of a certain motor in its columns, 
        // its rows are the pins in the following order 
        // 0=step,1=dir,2=enable,3 interrupt. Ie [2][0] is the step pin of the motor number 2

    AccelStepper stepper0(AccelStepper::DRIVER, STEPPER0_STEP_PIN, STEPPER0_DIR_PIN); //!< stepper 0
    AccelStepper stepper1(AccelStepper::DRIVER, STEPPER1_STEP_PIN, STEPPER1_DIR_PIN); //!< stepper 1


    AccelStepper steppers[] = {stepper0, stepper1}; //!< array that holds all the steppers

    // speed configurations
    int max_speeds[4] = {200, 200, 200, 200};    //!<  max speeds of the steppers, respectivly
    int accelerations[4] = {300, 300, 300, 300}; //!<  acceleration of the steppers, respectivly

    int enable_function(boolean is_writing, int mot_number, boolean enable_val)
    {
        /*! Read or set state of the enable pin of the stepper motors
        *
        *  @param is_writing false to read the state, true to change it
        *  @param mot_number number of motor to read or set
        *  @param enable_val Value to set, 0 to turn off or anything else to turn on
        *  @return 0 if is_writing is set to true or the value to be read if is_writing is false.
        */
        if (is_writing)
        {
            if (enable_val)
            {
                digitalWrite(STEPPER_PINS[mot_number][2],LOW);
            }
            else
            {
                digitalWrite(STEPPER_PINS[mot_number][2],HIGH);
            }
            return 0;
        }
        else
        {
            return digitalRead(STEPPER_PINS[mot_number][2]);
        }
    }

    int speed_function(boolean is_writing, int mot_number, int speed_value)
    {
        /*! Read or set state of max speed of the stepper motors
        *
        *  @param is_writing false to read the speed, true to change it
        *  @param mot_number number of motor to read or set the speed
        *  @param speed_value Value to set the speed
        *  @return 0 if is_writing is set to true or the value speed value of the motor
        */
        if (is_writing)
        {
            max_speeds[mot_number] = speed_value;
            steppers[mot_number].setMaxSpeed(max_speeds[mot_number]);
            return 0;
        }
        else
        {
            return max_speeds[mot_number];
        }
    }
    int acc_function(boolean is_writing, int mot_number, int acc_value)
    {
        /*! Read or set state of acceleration of the stepper motors
        *
        *  @param is_writing false to read the acceleration, true to change it
        *  @param mot_number number of motor to read or set the acceleration
        *  @param acc_value Value to set the acceleration
        *  @return 0 if is_writing is set to true or the current acceleration if false.
        */
        if (is_writing)
        {
            accelerations[mot_number] = acc_value;
            steppers[mot_number].setAcceleration(accelerations[mot_number]);
            return 0;
        }
        else
        {
            return accelerations[mot_number];
        }
    }

    int move_function(boolean is_writing, int mot_number, int steps)
    {
        /*! send the move command to the stepper motor or read distanceToGo()
        *
        *  @param is_writing false to read the distanceToGo(), true to call move()
        *  @param mot_number number of motor to read or set the move function
        *  @param steps argument to pass to move function
        *  @return 0 if is_writing is set to true or the distanceToGo() if false
        */
        if (is_writing)
        {
            steppers[mot_number].move(steps);
            return 0;
        }
        else
        {
            return steppers[mot_number].distanceToGo();
        }
    }
    void run_steppers(void){
        steppers[0].run();
        steppers[1].run();
    }
    void setup(void)
    {
        /*! Sets up motor and pins associated to the stepper motors.
         */
        for (int mot_number = 0; mot_number < 2; mot_number++)
        {
            pinMode(STEPPER_PINS[mot_number][0], OUTPUT);
            pinMode(STEPPER_PINS[mot_number][1], OUTPUT);
            pinMode(STEPPER_PINS[mot_number][2], OUTPUT);
            enable_function(true, mot_number, false);
            steppers[mot_number].setEnablePin(STEPPER_PINS[mot_number][3]);
            steppers[mot_number].setMaxSpeed(max_speeds[mot_number]);
            steppers[mot_number].setAcceleration(accelerations[mot_number]);
        }
    }
}