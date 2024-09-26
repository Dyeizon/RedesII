import sys
import requests

if(len(sys.argv) != 4):
    print('O número de argumentos é insatisfatório')
    sys.exit()

HOST = sys.argv[1]
PORT = sys.argv[2]
FILENAME = sys.argv[3]

print('{0}:{1} - {2}'.format(HOST, PORT, FILENAME))

URL = 'http://' + HOST + ':' + PORT
req = requests.get(URL)
print(req)