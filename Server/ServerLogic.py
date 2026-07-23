# imagine we have two puters in LAN

from mss import MSS

import socket
import json
import threading

import cotton_candy

from Coroutines.ListenCoroutine import ListenCoroutine
from Coroutines.ClientHandleCoroutine import ClientHandleCoroutine


class ServerLogic:
    def __init__(self, host='127.0.0.1', port=56677):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

        self.manager = cotton_candy.CoroutineManager(auto_start=True)

        print(self.manager.get_coroutine_classes_list())

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(10.0)
        self.manager.start()
        self.running = True

        res = self.manager.create_coroutine(
            ListenCoroutine,
            {"server_socket": self.server_socket}
        )
        print("ServerListenCoroutine", res)
        # res = self.manager.create_coroutine(
        #     ClientHandleCoroutine,
        #     {}
        # )
        # print("ClientHandleCoroutine", res)

        print(f"Сервер запущен на {self.host}:{self.port}")
        print("Ожидание подключений...")




    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        self.manager.shutdown(5)
        print("Сервер остановлен")
