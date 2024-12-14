import requests
import json
import socket

class UserLibrary:
    def __init__(self, server_ip, master_node_ip):
        self.server_ip = server_ip
        self.master_node_ip = master_node_ip
        self.user_ip = self._get_user_ip()
        self.user_id = None
        self.task_id = None
        self.status = None

    def _get_user_ip(self):
        # Получение IP-адреса пользователя
        return socket.gethostbyname(socket.gethostname())

    def initialize_user(self):
        # Запрос у пользователя ввода логина, пароля, данных для работы и функции в виде строки
        login = input("Введите ваш логин: ")
        password = input("Введите ваш пароль: ")
        work_data = input("Введите данные для работы: ")
        function = input("Введите функцию: ")

        # Сбор данных
        user_data = {
            'ip': self.user_ip,
            'login': login,
            'password': password,
            'data': work_data,
            'function': function
        }

        # Отправка данных на сервер
        self.send_to_server(user_data)

    def send_to_server(self, data):
        # Отправка JSON-данных на сервер
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.server_ip, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Данные отправлены на сервер успешно.")
        else:
            print(f"Не удалось отправить данные на сервер. Код состояния: {response.status_code}")

    def get_from_server(self):
        # Получение user_id и task_id с сервера
        response = requests.get(self.server_ip)
        if response.status_code == 200:
            data = response.json()
            self.user_id = data.get('user_id')
            self.task_id = data.get('task_id')
            print(f"Получен user_id: {self.user_id} и task_id: {self.task_id}")
        else:
            print(f"Не удалось получить данные с сервера. Код состояния: {response.status_code}")

    def send_to_master_node(self):
        # Отправка user_id и task_id на мастер-узел
        if self.user_id is None or self.task_id is None:
            print("user_id или task_id недоступны. Пожалуйста, сначала вызовите get_from_server.")
            return
        data = {
            'user_id': self.user_id,
            'task_id': self.task_id
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.master_node_ip, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print("Данные отправлены на мастер-узел успешно.")
        else:
            print(f"Не удалось отправить данные на мастер-узел. Код состояния: {response.status_code}")

    def get_from_master_node(self):
        # Получение статуса и task_id от мастер-узла
        response = requests.get(self.master_node_ip)
        if response.status_code == 200:
            data = response.json()
            self.status = data.get('status')
            self.task_id = data.get('task_id')
            print(f"Получен статус: {self.status} для task_id: {self.task_id}")
        else:
            print(f"Не удалось получить данные с мастер-узла. Код состояния: {response.status_code}")