import requests
import json
import socket
import csv
import time

class UserLibrary:
    def __init__(self, server_ip, master_node_ip, server_ip_get_res):
        self.server_ip = server_ip
        self.server_ip_get_res = server_ip_get_res
        self.master_node_ip = master_node_ip
        self.user_ip = self._get_user_ip()
        self.user_id = None
        self.task_id = None
        self.status = None

    def _get_user_ip(self):
        # Получение IP-адреса пользователя
        return socket.gethostbyname(socket.gethostname())


    def read_function_from_txt(self, txt_file):
        """
        Чтение функции из текстового файла.
        """
        with open(txt_file, mode='r', encoding='utf-8') as file:
            function = file.read()
        return function
    
    def read_data_from_csv(self, csv_file):
        """
        Чтение данных из CSV-файла и преобразование их во вложенный список.
        """
        nested_list = []
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок
            for row in reader:
                # Удаляем пустые элементы
                cleaned_row = [item for item in row if item]
                # Преобразуем элементы в вещественные числа
                float_row = [float(item) for item in cleaned_row]
                nested_list.append(float_row)
        return nested_list
    
    def initialize_user(self, txt_file, csv_file):
        # Запрос у пользователя ввода логина, пароля, данных для работы и функции в виде строки
        login = input("Введите ваш логин: ")
        password = input("Введите ваш пароль: ")
        #work_data = input("Введите данные для работы: ")
        #function = input("Введите функцию: ")

        function = self.read_function_from_txt(txt_file)
        if not function:
            print("Ошибка: не удалось прочитать функцию из текстового файла.")
            return
        
        # Чтение данных из CSV-файла и преобразование во вложенный список
        nested_list = self.read_data_from_csv(csv_file)
        if not nested_list:
            print("Ошибка: не удалось прочитать данные из CSV-файла.")
            return
        
        # Сбор данных
        user_data = {
            'ip': self.user_ip,
            'login': login,
            'password': password,
            'data': nested_list,
            'function': function
        }

        # Отправка данных на сервер
        self.send_to_server(user_data)

    def send_to_server(self, data):
        # Отправка JSON-данных на сервер
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.server_ip, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            self.user_id = response_data.get('user_id')
            self.task_id = response_data.get('task_id')
            print("Данные отправлены на сервер успешно.")
            print(f"Получен user_id: {self.user_id} и task_id: {self.task_id}")
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
        """
        Получение статуса и task_id от мастер-узла.
        Проверяет статус каждые 10 секунд, пока статус не станет "ready".
        """
        while True:
            response = requests.get(self.master_node_ip)
            if response.status_code == 200:
                data = response.json()
                self.status = data.get('status')
                self.task_id = data.get('task_id')
                print(f"Получен статус: {self.status} для task_id: {self.task_id}")

                # Проверяем, если статус "ready"
                if self.status == "ready":
                    print("Задача решена")
                    break
            else:
                print(f"Не удалось получить данные с мастер-узла. Код состояния: {response.status_code}")

            # Ждем 10 секунд перед следующей проверкой
            time.sleep(10)

        data_ser = {
            'user_id': self.user_id,
            'task_id': self.task_id,
        }

        # Отправка JSON-данных на сервер
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.server_ip_get_res, data=json.dumps(data_ser), headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            self.result = response_data.get('result')
            print(f"Результат вычислений: {self.result}")
        else:
            print(f"Не удалось отправить/получить с сервер. Код состояния: {response.status_code}")

    """
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
    """