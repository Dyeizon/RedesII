from socket import *
from time import sleep, time
import signal

HOST = '127.0.0.1'
PORT = 12000

def main():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    
    ping(serverSocket, 10)


def handle_timeout(_a, _b):
    raise TimeoutError


def ping(destination: socket, times: int):
    initial_time = time()

    signal.signal(signal.SIGALRM, handle_timeout)
    sent_pkgs = 0
    received_pkgs = 0

    for i in range(1, times+1):
        try:
            sleep(0.5)
            destination.sendto(f'Ping {i} {(time()- initial_time):.2f} segundos.'.encode('utf-8'), (HOST, PORT))
            sent_pkgs += 1

            signal.setitimer(signal.ITIMER_REAL, 0.75)

            msg, _ = destination.recvfrom(1024)
            received_pkgs += 1

            msg = msg.decode('utf-8')
            
            print(f'[{i}] {msg}')
        
        except (ConnectionRefusedError, TimeoutError):
            print(f'[{i}] Tempo limite excedido.')
            continue
        finally:
            signal.alarm(0)

    print(f'\n--- Estatísticas de ping para {HOST}:{PORT} ---')
    print(f'{sent_pkgs} pacotes transmitidos, {received_pkgs} recebidos, {((1 - received_pkgs/sent_pkgs) * 100):.0f}% de perda de pacotes, tempo de execução {(time() - initial_time):.2f}s')


main()