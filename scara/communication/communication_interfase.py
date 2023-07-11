"""
communication_interfase.py
    communication interfase to interact (locally or using tcp/ip)
    with the scara robot
"""
from .client import Client
from .server import Server

class CommunicationInterfase():
    """
    CommunicationInterfase class
    """
    def __init__(self):
        pass


    def start_server(self, server_ip, server_port):
        server = Server(ip=server_ip, port=server_port)
        server.start()
        while server.is_connected:
            server.handle_client()


    def start_client(self, client_ip, client_port):
        client = Client(ip=client_ip, port=client_port)
        client.start()
