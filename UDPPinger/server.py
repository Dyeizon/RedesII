from random import randint, uniform
from socket import *
from time import sleep, time

HOST = '127.0.0.1'
PORT = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((HOST, PORT))
print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))

while True:
    timer = time()

    rand = randint(0, 10)

    message, address = serverSocket.recvfrom(1024)

    if rand < 4:
        print('PING PERDIDO')
        continue
    
    # Simulando atraso de 0,05s a 0.09s

    serverSocket.sendto(message, address)