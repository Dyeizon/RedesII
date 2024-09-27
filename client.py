from socket import *
from sys import argv
import threading

def main():
    if(len(argv) != 4):
        print('Argumentos inconsistentes, siga o padrão:')
        print('{0} (dest) (port) (file)'.format(argv[0]))
        return
    
    HOST = argv[1]
    PORT = int(argv[2])
    FILE = argv[3]

    client = socket(AF_INET, SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
    except:
        return print('Erro ao conectar ao servidor.')

    threading.Thread(target=receive, args=[client]).start()
    threading.Thread(target=send, args=[client]).start()

def receive(client: socket):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg + '\n')
        except:
            print('Conexão perdida.\nPressione <Enter> para finalizar.')
            client.close()
            break

def send(client: socket):
    while True:
        try:
            msg = input('\n')
            client.send(msg.encode('utf-8'))

        except:
            return
        

main()