"""
client.py
    creates a client (local pc) for sending information to the raspy
    and move the scara
"""
import logging
import socket

from . import commands
#import commands

logger = logging.getLogger(__name__)

class Client():
    """
    Client class
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False


    def start(self):
        logger.info("starting client")
        self.client.connect(self.addr)
        self.is_connected = True


    def receive(self):
        try:
            msg_recv_encode = self.client.recv(commands.HEADERSIZE)
            msg_recv_decode = msg_recv_encode.decode(commands.FORMAT)
            logger.debug("response from server: %s", msg_recv_decode)
        except Exception as e:
            logger.error("Exception: %s", e)


    def send(self, msg):
        logger.debug("sending message")
        msg_encode = msg.encode(commands.FORMAT)
        self.client.send(msg_encode)


    def check_for_disconnect(self, msg):
        if msg == commands.DISCONNECT_MESSAGE:
            self.client.close()
            self.is_connected = False
            logger.info("connection closed")


    def handle_server_once(self, msg_decode):
        logger.debug("handling server with addres %s", self.addr)
        self.send(msg_decode)
        self.receive()
        self.check_for_disconnect(msg_decode)


    def handle_server_interactively_once(self):
        logger.debug("handling server with addres %s", self.addr)
        msg_decode = input("message to the server? \n")
        self.send(msg_decode)
        self.receive()
        self.check_for_disconnect(msg_decode)


    def handle_server_interactively_continously(self):
        while self.is_connected:
            self.handle_server_once()


if __name__ == "__main__":
    client = Client(ip="127.0.0.1", port=1025)
    client.start()
    client.handle_server_continously()
