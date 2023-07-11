"""
communication_interfase.py
    communication interfase to interact (locally or using tcp/ip)
    with the scara robot
"""
import logging

import scara
from .client import Client
from .server import Server


logger = logging.getLogger(__name__)

IP = "127.0.0.1"
PORT = 1025

class CommunicationInterfase():
    """
    CommunicationInterfase class
    """
    def __init__(self, robot: scara.Robot = None):
        self.robot = robot


    ## Runs in the client's side
    def start_client(self,
                   client_ip=IP,
                   client_port=PORT):
        self.client = Client(ip=client_ip, port=client_port)
        self.client.start()


    def send_msg_to_server_interactively(self, mode="once"):
        if mode == "once":
            self.client.handle_server_interactively_once()
        elif mode == "continously":
            self.client.handle_server_interactively_continously()
        else:
            logger.error("only 'once' and 'continously' mode supported")


    def send_msg_from_client_to_server(self, msg: str):
        #wrapped_msg = wrapper(service=666, params_dict=msg)
        #dumped_msg = dump(wrapped_msg)
        self.client.handle_server_once(msg_decode=dumped_msg)


    def send_msg_from_client_to_robot(self, service_id: int, **kargs):
        #wrapped_msg = wrapper(service=service_id, params_dict=kargs)
        #dumped_msg = dump(wrapped_msg)
        #self.client.handle_server_once(msg_decode=dumped_msg)


    ## Runs in the server's side
    def start_server(self,
                   server_ip=IP,
                   server_port=PORT):
        self.server = Server(ip=server_ip, port=server_port)
        self.server.start()
        while self.server.is_connected:
            msg_decode = self.server.handle_client_once()
            #msg_unwrapped = unwrapper(msg_decode)
            #if msg_unwrapped is a robot service
            try:
                self.send_msg_to_robot(msg_decode)
            except Exception as e:
                logger.error("Exception: %s", e)


    def send_msg_from_server_to_robot(self, msg):
        # dictionary with function's names and values
        self.robot.move2(2, 3, 1)
