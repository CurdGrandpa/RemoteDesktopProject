import socket

import cotton_candy


class ListenCoroutine(cotton_candy.BaseLoopCoroutine):
    def __init__(self, server_socket: socket.socket, shared_state_key: str = "clients", *args, **kwargs):
        super().__init__(interval=20, *args, **kwargs)
        self.shared_state_key = shared_state_key
        self.server_socket = server_socket

    async def setup_func(self):
        await super().setup_func()
        if cotton_candy.shared_state.get(self.shared_state_key) is None:
            cotton_candy.shared_state.set(self.shared_state_key, {"clients": []})
        print("Listen coroutine set up")
        print(vars(self))

    async def finish_func(self):
        print("finish ListenCoroutine")
        await super().finish_func()
        cotton_candy.shared_state.set(self.shared_state_key, None)

    async def loop_func(self):
        try:
            print("Listen coroutine loop func")
            print(cotton_candy.shared_state.get(self.shared_state_key))

            if not self.server_socket:
                return

            client_socket, address = self.server_socket.accept()

            print(f"Подключен клиент: {address}")
            print(client_socket)

            state = cotton_candy.shared_state.get(self.shared_state_key)
            state["clients"].append({
                "id": max([a["id"] for a in state["clients"]] + [0]) + 1,
                "client_socket": client_socket,
                "address": address
            })
            cotton_candy.shared_state.set(self.shared_state_key, state)
            print(state)

            # # Запускаем обработку клиента в отдельном потоке
            # client_thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            # client_thread.daemon = True
            # client_thread.start()
            print("Listen coroutine loopFunc ended")
        except socket.timeout:
            print("Тайм-аут ожидания подключения")
        except OSError as e:
            print("OSError")
            print(e.__class__)
            # print(e.__class__.errno)
            print(e.args)
            print(e)
        except Exception as e:
            print(f"Ошибка при принятии соединения:")
            print(e)
            await self.finish_func()
