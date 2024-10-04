from random import randint
from socket import *
from time import sleep

HOST = '127.0.0.1'
PORT = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))
print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))

while True:
    rand = randint(0, 10)

    message, address = serverSocket.recvfrom(1024)

    message = message.upper()

    if rand < 4:
        print('PING PERDIDO')
        continue

    serverSocket.sendto(message, address)