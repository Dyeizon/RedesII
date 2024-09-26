from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)

# Preparar o socket do servidor
HOST = '127.0.0.1'
PORT = 8001
origin = (HOST, PORT)
serverSocket.bind(origin)
serverSocket.listen(1)

while True:
    print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        
        if not message:
            break

        filename = message.split()[1]
        
        f = open(filename[1:])

        outputdata = f.read()

        connectionSocket.send(b'HTTP/1.1 200 OK\r\n')
        connectionSocket.send(b'Content-Type: text/html\r\n')
        connectionSocket.send(b'\r\n')

        for i in range(0, len(outputdata)):
           connectionSocket.send(outputdata[i].encode())

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Enviar mensagem de resposta para arquivo não encontrado
        connectionSocket.send(b'HTTP/1.1 404 NOT FOUND\r\n')
        connectionSocket.send(b'Content-Type: text/html\r\n')
        connectionSocket.send(b'\r\n')

        connectionSocket.send(b'<html><body><h1>Error 404: Not Found</h1></body></html>\r\n')

        # Fechar o socket do cliente
        connectionSocket.close()

print("Fechando conexão")
serverSocket.close()
sys.exit()