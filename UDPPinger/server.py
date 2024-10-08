from random import randint
from socket import *
from time import time
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))
print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))

def check_beat(last_ping: str) -> bool:
    print(f'Agora: {datetime.now()} - Ping {last_ping}')
    return True

while True:
    timer = time()

    rand = randint(0, 10)

    message, address = serverSocket.recvfrom(1024)

    if rand < 4:
        print('PING PERDIDO')
        continue

    message_splitted = message.decode('utf-8').split(' ')
    last_ping = message_splitted[2] + ' ' + message_splitted[3]
    check_beat(last_ping)
    
    serverSocket.sendto(message, address)