from socket import *
from time import sleep
import threading
import os

HOST = '127.0.0.1'
PORT = 8000

def main():
    server = startServer(PORT)
    if not server: return
    
    print('Servidor rodando no endereço {0}:{1}'.format(HOST, PORT))
    
    while True:
        conn, addr = server.accept()
        print(f'Conexão recebida de {addr}')
        
        threading.Thread(target=runParallelChannel, args=(conn, addr)).start()

def startServer(port: int):
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((HOST, port))
        server.listen()
        return server
    except Exception as e:
        print('Erro ao inicializar o servidor:', e)
        return None

def runParallelChannel(conn: socket, addr: list):
    try:
        message = conn.recv(1024).decode('utf-8')
        
        if not message:
            print(f'Conexão encerrada por {addr}')
            return

        filename = message.split()[1]
        print(f'[sleep] Simulando tempo de execução da requisição do cliente {addr[0]}:{addr[1]}...')

        sleep(10)

        print(f'Enviando {filename} para {addr[0]}:{addr[1]}')

        if os.path.isfile(filename[1:]):
            with open(filename[1:], 'r') as f:
                outputdata = f.read()

            conn.sendall('HTTP/1.1 200 OK\r\n'.encode('utf-8'))
            conn.sendall('Content-Type: text/html\r\n'.encode('utf-8'))
            conn.sendall('\r\n'.encode('utf-8'))
            conn.sendall(outputdata.encode('utf-8'))
        else:
            conn.sendall('HTTP/1.1 404 NOT FOUND\r\n'.encode('utf-8'))
            conn.sendall('Content-Type: text/html\r\n'.encode('utf-8'))
            conn.sendall('\r\n'.encode('utf-8'))
            conn.sendall('<html><body><h1>Error 404: Not Found</h1></body></html>\r\n'.encode('utf-8'))

    except Exception as e:
        print(f'Erro ao processar a conexão com {addr}: {e}')
    finally:
        conn.close()
        print(f'Conexão encerrada com {addr}')


main()