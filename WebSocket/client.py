from socket import *
from sys import argv

def main():
    if(len(argv) != 4):
        print('Argumentos inconsistentes, siga o padrão:')
        print(f'{argv[0]} [dest] [port] [filename]')
        return
    
    HOST = argv[1]
    PORT = int(argv[2])
    FILE = argv[3]

    client = socket(AF_INET, SOCK_STREAM)
    
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        return print('Erro ao conectar ao servidor:', e)

    openFile(client, FILE)

    receive(client)


def openFile(client: socket, filename: str):
    try:
        client.send(f'GET /{filename} HTTP/1.1'.encode('utf-8'))
    except:
        print('Erro ao enviar a mensagem para a renderização do arquivo')
        return

def receive(client: socket):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if(msg):
                print(msg, end='')
        except:
            break

    print('Conexão perdida.')
    client.close()
main()