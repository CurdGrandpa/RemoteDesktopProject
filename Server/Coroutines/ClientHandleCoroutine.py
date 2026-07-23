import json

import cotton_candy


class ClientHandleCoroutine(cotton_candy.BaseLoopCoroutine):
    def __init__(self, shared_state_key: str = "clients", *args, **kwargs):
        super().__init__(interval=10, *args, **kwargs)
        self.shared_state_key = shared_state_key


    async def loop_func(self):
        print("ClientHandle loopFunc")
        state = cotton_candy.shared_state.get(self.shared_state_key)
        if state is None:
            return

        for client in state.get("clients", []):

            # Получаем данные
            data = client["client_socket"].recv(1024).decode('utf-8')
            if not data:
                break

            # Парсим JSON
            try:
                received_json = json.loads(data)
                print(f"Получено от {client["address"]}: {received_json}")

                # Формируем ответ
                response = {
                    "status": "success",
                    "message": "JSON получен",
                    "received_data": received_json,
                    "server_time": "2024-01-01 12:00:00"
                }

                # Отправляем ответ
                client["client_socket"].send(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                error_response = {
                    "status": "error",
                    "message": "Неверный формат JSON"
                }
                client["client_socket"].send(json.dumps(error_response).encode('utf-8'))
        print("ClientHandle loopFunc finished")

    async def finish_func(self):
        await super().finish_func()
        print("Client Handle finish func")
        state = cotton_candy.shared_state.get(self.shared_state_key)
        if state is None:
            return

        for client in state.get("clients", []):
            try:
                client["client_socket"].close()
                print(f"Клиент {client["address"]} отключен")
            except Exception as e:
                print(e)
