
namespace can{
    void init();
    void decide(uint8_t buffer[], uint8_t size);
    int check_for_messages();
    uint8_t buffer[8];
}