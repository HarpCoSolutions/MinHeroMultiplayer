import random

import matplotlib
import numpy as np
from min_hero_classes import Minion, BaseMinion, Gem

import socket
import threading
import ast
matplotlib.use('Agg')  # Use a non-interactive backend


def is_ally(minion_id, minions):
    for minion in minions:
        if minion["minion_id"] == minion_id:
            return minion["side"] == "ally"
    return False


def select_target_positions(minions, is_ally_turn):
    valid_positions = []
    for minion in minions:
        if minion["currHealth"] > 0:
            if (is_ally_turn and minion["side"] == "enemy") or (not is_ally_turn and minion["side"] == "ally"):
                valid_positions.append(minion["position"])
    return valid_positions


class GameSocketServer:
    def __init__(self, host='localhost', port=12345,):
        self.host = host
        self.port = port
        self.server_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Game server started, waiting for connections...")

        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        move_ids = None
        minions = []
        minion_id = None
        turn_count = 0
        try:
            while True:
                data = str(client_socket.recv(8192).decode('utf-8'))
                if turn_count == 0:
                    print(data.replace('null', "None").replace("true", "True").replace("false", "False"))
                    minion = Minion.from_dict(ast.literal_eval(data.replace('null', "None").replace("true", "True").replace("false", "False")))
                    self.send_data(client_socket, minion.to_custom_string())
                    turn_count+=1


        except ConnectionResetError as e:
            print(e)
            pass
        finally:
            client_socket.close()
            self.server_socket.close()
            print("closed")

    @staticmethod
    def send_data(client_socket, message):
        try:
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent data: {message}")
        except Exception as e:
            print(f"Failed to send data: {e}")


if __name__ == "__main__":
    server = GameSocketServer()
    server.start_server()
