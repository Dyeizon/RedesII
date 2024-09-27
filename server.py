from socket import *
import sys
import threading

clients: list[socket] = []

# Preparar o socket do servidor
server = socket(AF_INET, SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 8005

try:
    server.bind((HOST, PORT))
    server.listen()
    print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))
except:
    print('Erro ao rodar o servidor.')
    sys.exit()

while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(clients)

    try:
        message = conn.recv(1024)
        
        if not message:
            break

        filename = message.split()[1]
        
        f = open(filename[1:])

        outputdata = f.read()

        conn.send('HTTP/1.1 200 OK\r\n'.encode('utf-8'))
        conn.send('Content-Type: text/html\r\n'.encode('utf-8'))
        conn.send('\r\n'.encode('utf-8'))

        for i in range(0, len(outputdata)):
           conn.send(outputdata[i].encode('utf-8'))

        conn.send("\r\n".encode('utf-8'))
        conn.close()

    except IOError:
        # Enviar mensagem de resposta para arquivo não encontrado
        conn.send('HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8'))
        conn.send('Content-Type: text/html\r\n'.encode('utf-8'))
        conn.send('\r\n'.encode('utf-8'))

        conn.send('<html><body><h1>Error 404: Not Found</h1></body></html>\r\n'.encode('utf-8'))

        # Fechar o socket do cliente
        conn.close()

print("Conexão encerrada.")
server.close()
sys.exit()