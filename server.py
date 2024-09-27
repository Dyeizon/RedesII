from socket import *
import threading

clients: list[socket] = []
HOST = '127.0.0.1'
PORT_WEB = 8000

def main():
    server = startServer(HOST, PORT_WEB)
    if(not server): return

    #threading.Thread(target=webCommunication, args=[server]).start()
    
    threading.Thread(target=webCommunication, args=[server]).start()

def startServer(host: str, port: int):
    try:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((host, port))
        server.listen()
        print('Servidor rodando no endereço {0}:{1}'.format(host, port))
        return server
    except:
        print('Erro ao inicializar o servidor.')
        return None

def webCommunication(server: socket):
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        #print(clients)

        try:
            message = conn.recv(1024).decode('utf-8')
            
            if not message:
                break

            filename = message.split()[1]
            print(f'Enviando {filename} para {addr[0]}:{addr[1]}')
            
            f = open(filename[1:])

            outputdata = f.read()

            conn.send('HTTP/1.1 200 OK\r\n'.encode('utf-8'))
            conn.send('Content-Type: text/html\r\n'.encode('utf-8'))
            conn.send('\r\n'.encode('utf-8'))

            for i in range(0, len(outputdata)):
                conn.send(outputdata[i].encode('utf-8'))

            conn.send("\r\n".encode('utf-8'))
            conn.close()

        except BrokenPipeError:
            print('Não foi possível enviar a mensagem ao cliente.')
            conn.close()
            return

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

main()