"""
client.py
    creates a client (local pc) for sending information to the raspy
    and move the scara
"""
import logging
import socket

from . import commands

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
            self.is_connected = False


    def handle_server(self):
        logger.debug("handling server with addres %s", self.addr)
        while self.is_connected:
            msg_decode = input("message to the server? \n")
            self.check_for_disconnect(msg_decode)
            self.send(msg_decode)
            self.receive()
        self.client.close()


if __name__ == "__main__":
    client = Client(ip="127.0.0.1", port=1025)
    client.start()
    while client.is_connected:
        client.handle_server()
