##server side
import socket
import threading

#----------GLOBAL VARS------------------
PORT = 9999
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MSG = '!CONNECT'
ALL_CLIENTS = []
#---------------------------------------


def server_success_message():
    print('=============================')
    print(':: SERVER SETUP SUCCESSFUL ::')
    print('=============================')


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
#-----------------------------------SERVER FUNCTIONS-------------------------------------------
def handle_client(client,addr):
    global ALL_CLIENTS

    USERNAME = None
    connected = True

    while connected:
        message_length = client.recv(HEADER).decode(FORMAT)
        if message_length:
            message_length = int(message_length)
            message = client.recv(message_length).decode(FORMAT)

            if not USERNAME:
                USERNAME = message
                print(f'[NEW CONNECTION] :: {USERNAME} connected.')
            else:
                if message==DISCONNECT_MSG:
                    connected = False
                else:
                    for user in ALL_CLIENTS:
                        if user!=client:
                            send_message(user, message)


    try:
        ALL_CLIENTS.remove(client)
    except:
        pass

    client.close()
    print(f'[LEAVING] :: {USERNAME} left the room.')
    print(f'[ACTIVE CONNECTIONS] :: {threading.activeCount() - 1}')



def start_server():
    global ALL_CLIENTS

    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print('[STARTING] :: Server is starting...')
    server.listen()
    server_success_message()
    print(f'[LISTENING] :: Server is listening on {IP}')

    while True:
        client, addr = server.accept()
        ALL_CLIENTS.append(client)
        thread = threading.Thread(target=handle_client, args=(client,addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] :: {threading.activeCount()-1}')





# ------------------main------------------------------------------------------------------------------
#SERVER SIDE

start_server()

