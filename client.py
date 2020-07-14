## client side
import socket
import threading

#----------GLOBAL VARS------------------
PORT = 9999
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MSG = '!CONNECT'
#ALL_CLIENTS = []
#---------------------------------------

def welcome_client_message():
    print('===============================')
    print(':: WELCOME TO LOCAL CHATROOM ::')
    print('===============================')


def initialize(port=9999, format='utf-8', header=64, disconnect_msg='!CONNECT'):
    global PORT, FORMAT, HEADER, DISCONNECT_MSG

    PORT = port
    FORMAT = format
    HEADER = header
    DISCONNECT_MSG = disconnect_msg


def send_message(client, msg):
    message = msg.encode(FORMAT)
    message_length = len(message)
    encoded_message_length = str(message_length).encode(FORMAT)
    encoded_message_length += b' ' * (HEADER - len(encoded_message_length))
    client.send(encoded_message_length)
    client.send(message)


def receive_message(client):
    message_length = client.recv(HEADER).decode(FORMAT)
    if message_length:
        message_length = int(message_length)
        message = client.recv(message_length).decode(FORMAT)
        print(f'{message}')



################################################################################################


def start_client(ip):
    IP = ip  ## of the server
    ADDR = (IP, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    welcome_client_message()

    USERNAME = input('[ENTER USERNAME] :: ')
    send_message(client, USERNAME)

    message = ''
    while message != DISCONNECT_MSG:
        ## to be updated
        message = input(f'[{USERNAME}] >> ')
        send_message(client, message)
        receive_message(client)


# ---------------------------------------------------------------------------------------------------




# ------------------main------------------------------------------------------------------------------

#CLIENT SIDE
initialize(port=9999, header=64)
server_ip = '192.168.10.39'
start_client(server_ip)
