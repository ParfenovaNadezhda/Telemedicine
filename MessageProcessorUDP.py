from threading import Thread
import time
import ast
import socket
import time
import json

class MessageProcessor():
    def __init__(self, ip, port):
        self.init_msg = b'hello world'
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.logins = {}

    def init_network(self):
        self.sock_init = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_init.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        for _ in range(5):
            self.sock_init.sendto(self.init_msg, ("255.255.255.255", 5005))
            time.sleep(1)
        self.sock_init.close()
            
    def send_message(self, ip, port, msg):
        self.sock.sendto(msg, (ip, port))

    def get_message(self):
        self.sock.bind((self.ip, self.port))
        while True:
            data, addr = self.sock.recvfrom(1024)
            print('Got message from', addr)
            self.parse_message(data, addr)
        
    def register_login(self, login, ip, port):
        self.logins[login] = (ip, port)
        return

    def return_logins(self):
        byte_msg = json.dumps(self.logins).encode()
        return byte_msg
    
    def parse_message(self, msg, addr):
        msgs = msg.decode()
        msg_dict = ast.literal_eval(msgs)
        if msg_dict['msg_type'] == 'intro':
            self.register_login(msg_dict['login_from'], addr[0], addr[1])
            print("Login {} registered for ip {}".format(msg_dict['login_from'], addr[0]))
        elif msg_dict['msg_type'] == 'logins':
            byte_msg = self.return_logins()
            self.send_message(addr[0], addr[1], byte_msg)
            print('Logins sent to {}'.format(msg_dict['login_from']))
        elif msg_dict['msg_type'] == 'msg':
            ip_to, port_to = self.logins[msg_dict['login_to']]
            self.send_message(addr[0], addr[1], msg_dict['msg'].encode())
            print('Message from {} sent to {}'.format(msg_dict['login_from'], msg_dict['login_to']))
            
msgprcr = MessageProcessor('0.0.0.0', 5005)
while True:
    msgprcr.get_message()
    time.sleep(1)