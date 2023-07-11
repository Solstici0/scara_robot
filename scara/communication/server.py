"""
server.py
    creates a server (in the raspy) for receiving information and move the scara
"""
import logging
import socket

from . import commands

logger = logging.getLogger(__name__)

class Server():
    """
    Server class
    """
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False


    def start(self):
        logger.info("starting server")
        self.server.bind(self.addr)
        self.server.listen()
        self.is_connected = True


    def receive(self):
        try:
            msg_encode = self.conn.recv(commands.HEADERSIZE)
        except Exception as e:
            logger.error("Exception: %s", e)
        return msg_encode


    def send(self, msg_encode):
        msg_decode = msg_encode.decode(commands.FORMAT)
        response_decode = f"The message from client was: {msg_decode}"
        response_encode = response_decode.encode(commands.FORMAT)
        self.conn.send(response_encode)
        logger.debug("response to the client: %s", response_decode)


    def check_for_disconnect(self, msg):
        if msg == commands.DISCONNECT_MESSAGE.encode(commands.FORMAT):
            self.is_connected = False

    def handle_client(self):
        self.conn, self.addr = self.server.accept()
        logger.debug("handling client with address %s", self.addr)
        while self.is_connected:
            msg_encode = self.receive()
            self.check_for_disconnect(msg_encode)
            self.send(msg_encode)
        self.conn.close()


if __name__ == "__main__":
    server = Server(ip="127.0.0.1", port=1026)
    server.start()
    while server.is_connected:
        server.handle_client()
