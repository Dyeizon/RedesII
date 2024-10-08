from random import randint
from socket import *
from time import time
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))
print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))

def check_beat(seconds_difference: int, last_ping_timestamp: int) -> bool:
    print(f'Agora: {datetime.now()} - Ping {datetime.fromtimestamp(last_ping_timestamp)}')

    print('diff:', (datetime.now() - datetime.fromtimestamp(last_ping_timestamp)))
    
    return True

while True:
    timer = time()

    rand = randint(0, 10)

    message, address = serverSocket.recvfrom(1024)

    if rand < 4:
        print('PING PERDIDO')
        continue

    message_splitted = message.decode('utf-8').split(' ')
    print(message_splitted)
    last_ping_timestamp = int(message_splitted[2])

    check_beat(5, last_ping_timestamp)
    
    serverSocket.sendto(message, address)