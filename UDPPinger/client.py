from socket import *
from time import time, sleep
from datetime import datetime
import signal
from math import inf

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

    rtts = []

    for i in range(1, times+1):
        try:
            sleep(0.7)
            send_time = time()
            destination.sendto(f'Ping seq={i} {int(datetime.now().timestamp())}'.encode('utf-8'), (HOST, PORT))
            sent_pkgs += 1

            signal.alarm(1)

            msg, _ = destination.recvfrom(1024)
            received_pkgs += 1

            rtt = time() - send_time
            rtts.append(rtt)

            print(f"{msg.decode('utf-8')} RTT={rtt * 1000:.3f}ms")
        
        except (ConnectionRefusedError, TimeoutError):
            print('Tempo limite excedido.')
            signal.alarm(0)
            continue
        finally:
            signal.alarm(0)

    print(f'\n--- Estatísticas de ping para {HOST}:{PORT} ---')
    print(f'{sent_pkgs} pacotes transmitidos, {received_pkgs} recebidos, {((1 - received_pkgs/sent_pkgs) * 100):.0f}% de perda de pacotes, tempo de execução {(time() - initial_time):.2f}s')
    print(f'rtt min/avg/max = {calc_min_rtt(rtts) * 1000:.3f}/{calc_avg_rtt(rtts) * 1000:.3f}/{calc_max_rtt(rtts) * 1000:.3f} ms')

def calc_min_rtt(rtts: list):
    if len(rtts) == 0: return 0
    minimum = float('inf')

    for rtt in rtts:
        if (rtt < minimum):
            minimum = rtt
    
    return minimum

def calc_max_rtt(rtts: list):
    if len(rtts) == 0: return 0
    maximum = float('-inf')
    for rtt in rtts:
        if (rtt > maximum):
            maximum = rtt
    
    return maximum

def calc_avg_rtt(rtts: list):
    if len(rtts) == 0: return 0
    sum = 0
    count = 0
    for rtt in rtts:
        count += 1
        sum += rtt

    return sum/count

main()