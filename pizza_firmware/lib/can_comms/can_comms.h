#include <stdio.h>
namespace can{
    
    /**
     * @brief This function should initialize the spi comunicaction with the CAN driver
     * and set a filter for the adress of the device, only the messages with such adress
     * should be processed by this namespace
     * 
     * @param address Filtering address
     */
    void init(uint16_t address);

    /**
     * @brief process the received buffer and executes the corresponding function
     * 
     * @param buffer the buffer where the CAN payload is stored
     * @param size size of the payload
     */
    void decide(uint8_t buffer[], uint8_t size);

    /**
     * @brief Fills buffer with the payload of the last CAN message
     * 
     * @param buffer the buffer where the CAN payload is stored
     * @param size size of the payload
     */
    void dump_messages(uint8_t buffer[], uint8_t size);

    /**
     * @brief check the device to see if a new valid can message was received
     * 
     * @return int the number of received payload, -1 if no new payload
     */
    int check_for_messages();

    /**
     * @brief internal buffer to fill with new CAN messages
     * 
     */
    uint8_t buffer[8];

    /**
     * @brief size of the last received byte
     * 
     */
    uint8_t size;

    /**
     * @brief structure data type to fill with the stepper functions
     * 
     */
    typedef struct 
    {
        int (*enable) (bool is_writing, int mot_number, bool enable_val);
        int (*speed) (bool is_writing, int mot_number, bool enable_val);
        int (*acc) (bool is_writing, int mot_number, bool enable_val);
        int (*move) (bool is_writing, int mot_number, bool enable_val);
        /* data */
    }stepperFunctions_t;

    /**
     * @brief structure data type to fill with the servo functions
     * 
     */
    typedef struct 
    {
        int (*enable) (bool is_writing, int mot_number, bool enable_val);
        int (*speed) (bool is_writing, int mot_number, bool enable_val);
        int (*acc) (bool is_writing, int mot_number, bool enable_val);
        int (*move) (bool is_writing, int mot_number, bool enable_val);
        /* data */
    }servoFunctions_t;

    /**
     * @brief structure data type to fill with the digital output functions
     * 
     */
    typedef struct 
    {
        int (*state) (bool is_writing, int mot_number, bool enable_val);
        /* data */
    }digitalOutputFunctions_t;

    /**
     * @brief object with the stepper functions
     * 
     */
    stepperFunctions_t stepperFunctions;

    /**
     * @brief object with the servo functions
     * 
     */
    servoFunctions_t servoFunctions;

    /**
     * @brief object with the digital output functions
     * 
     */
    digitalOutputFunctions_t digitalOutputFunctions;

    



    
}