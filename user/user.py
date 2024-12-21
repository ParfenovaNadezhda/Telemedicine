from bibla import UserLibrary

def main():
    # Укажите IP-адреса сервера и мастер-узла
    server_ip = 'http://192.168.17.178:5000/api/user'  # Замените на реальный URL сервера
    master_node_ip = 'http://192.168.52.178:5000/api/master'  # Замените на реальный URL мастер-узла
    server_ip_get_res = 'http://192.168.17.178:5000/api/user_res'

    txt_file = 'function.txt'  # Путь к текстовому файлу
    csv_file = 'data.csv'

    # Создаем экземпляр класса UserLibrary
    user_lib = UserLibrary(server_ip, master_node_ip, server_ip_get_res)

    # Инициализация пользователя
    user_lib.initialize_user(txt_file, csv_file)

    # Получение user_id и task_id с сервера
   # user_lib.get_from_server()

    # Отправка user_id и task_id на мастер-узел
    user_lib.send_to_master_node()

    # Получение статуса и task_id от мастер-узла
    user_lib.get_from_master_node()

if __name__ == "__main__":
    main()