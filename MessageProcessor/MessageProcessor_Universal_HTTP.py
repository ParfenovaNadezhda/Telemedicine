from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import threading
import argparse
import requests
import json
import time
import ast


class Server(HTTPServer):
    def __init__(self, address, request_handler):
        super().__init__(address, request_handler)


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server_class):
        self.server_class = server_class
        super().__init__(request, client_address, server_class)

    def do_GET(self):
        response = {"Message status": "got"}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(dumps(response))))
        self.end_headers()
        self.wfile.write(str(response).encode('utf8'))

    def do_POST(self):
        response = {"Message status": "got"}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(dumps(response))))
        self.end_headers()
        self.wfile.write(str(response).encode('utf8'))
        content_len = int(self.headers.get('Content-Length'))
        post_body  = self.rfile.read(content_len)
        global dikt
        dikt = ast.literal_eval(post_body.decode().split('}')[0]+'}')
        if dikt['login_to'] == my_server_ip:
            print('Получено сообщение:', dikt['msg'])
            try:
                task_admin = TaskAdmin()
                task_admin.create_task(dikt['msg']['user_id'], dikt['msg']['task_id'], dikt['msg']['nodes'])
                # Task(...)
                # msg_count += 1 # можно использовать в качестве "флага" при отсутствии возможности создания класса
            try:
                micro_task_admin = MicroTaskAdmin(dikt['msg']['user_id'], dikt['msg']['task_id'], dikt['msg']['arr'], dikt['msg']['start_arr'], dikt['msg']['stop_arr'], dikt['msg']['function'], dikt['msg']['status'])
                # msg_count += 1 # можно использовать в качестве "флага" при отсутствии возможности создания класса     
        else:
            r = requests.post('http://'+str(dikt['login_to'])+':5005', json.dumps(dikt))    


def start_server(addr, port, server_class=Server, handler_class=RequestHandler):
    server_address = (addr, port)
    http_server = server_class(server_address, handler_class)
    print(f"Starting server on {addr}:{port}")
    http_server.serve_forever()

def send_message(server_ip, m):
    time.sleep(5) 
    response = requests.post(server_ip, json.dumps(m), verify = False)    


def main():
    global my_server_ip
    my_server_ip = '192.168.1.150'
    start_server(addr = my_server_ip, port = 5005)


if __name__ == "__main__":
    thread1 = threading.Thread(target = main)
    thread1.start()
    thread2 = threading.Thread(target = send_message(server_ip = 'http://192.168.1.122:5005', m = {       
       "login_to": "192.168.1.122",
       "msg": "Proverka",
       "user_id": "",
       "task_id": "",
       "arr": "",
       "arr_start": "",
       "arr_stop": "", 
       "function": "",
       "status": "",
       "nodes": "",
       "res": ""
   }))
    thread2.start()
    thread2.join()
    
    
'''
-------------------------------
Пояснения для MessageProcessor():
-------------------------------
1. Необходимо, чтобы в общем доступе были ip каждого сервера, они в дальнейшем указываются в разделе "login to" универсального сообщения
2. Для корректной работы программы необходимо менять только значение переменной my_server_ip
3. Для каждого сервера используется port = 5005
4*. Не забываем отключать брандмауэр, если программа выдаёт ConnectionError
5*. В этой версии программы второй поток используется для отправки тествого сообщения; часть кода, посвящённого thread2, в дальнейшем можно убрать

-------------------------------
Шаблон универсального сообщения:
-------------------------------
    
m = {
       
       "login_to": "192.168.14.134",
       "msg": "Proverka",
       "user_id": "",
       "task_id": "",
       "arr": "",
       "arr_start": "",
       "arr_stop": "", 
       "function": "",
       "status": "",
       "nodes": "",
       "res": ""
   }

'''