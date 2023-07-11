"""
server_interfase.py
    run this script to setup the raspy as server and command the robot
"""
import scara


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-ah", "--ahardware", help="hardware for a joint",
                        type=str, choices=["real", "fake"], default="fake")
    parser.add_argument("-zh", "--zhardware", help="hardware for z joint",
                        type=str, choices=["real", "fake"], default="fake")
    parser.add_argument("-ch", "--codohardware", help="hardware for codo joint",
                        type=str, choices=["real", "fake"], default="fake")
    parser.add_argument("-hh", "--hombrohardware", help="hardware for hombro joint",
                        type=str, choices=["real", "fake"], default="fake")
    parser.add_argument("-f", "--configfile", help="configuration file for the robot",
                        default="default", type=str)
    args = parser.parse_args()

    hardware_types = {"a": args.ahardware,
                      "z": args.zhardware,
                      "codo": args.codohardware,
                      "hombro": args.hombrohardware}
    #a_hw =
    nelen = scara.Robot(config_file=args.configfile,
                        #hombro_hw=hombro_hw,
                        #codo_hw=codo_hw,
                        #z_hw=z_hw,
                        #a_hw=a_hw
                        )

    server_handler = scara.communication.CommunicationInterfase(robot=nelen)
    server_handler.start_server()
