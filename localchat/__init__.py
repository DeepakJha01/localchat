
#----------IMPORTS----------------------
import socket
import threading

#----------GLOBAL VARS------------------
PORT = 9999
FORMAT = 'utf-8'
HEADER = 64
DISCONNECT_MSG = '!CONNECT'
ALL_CLIENTS = []
ALL_USERNAMES = []
#---------------------------------------


#---MESSAGES----------------------------
def server_success_message():
    print('=============================')
    print(':: SERVER SETUP SUCCESSFUL ::')
    print('=============================')

def welcome_client_message(user):
    print('================================' + '='*len(user))
    print(f':: WELCOME TO LOCAL CHATROOM {user} ::')
    print('================================' + '='*len(user))

def goodbye_client_message(user):
    print('===================' + '='*len(user))
    print(f':: SEE YOU SOON {user} ::')
    print('===================' + '='*len(user))
#----------------------------------------


#--to custom change global variables
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
#-----------------------------------SERVER FUNCTIONS--------------------------------------------
def broadcast(message):
    for user in ALL_CLIENTS:
        send_message(user,message)


def handle_client(client, addr):
    global ALL_CLIENTS
    global ALL_USERNAMES

    USERNAME = None
    connected = True

    while connected:
        try:
            message_length = client.recv(HEADER).decode(FORMAT)
            if message_length:
                message_length = int(message_length)
                message = client.recv(message_length).decode(FORMAT)

                if not USERNAME:
                    USERNAME = message
                    ALL_USERNAMES.append(USERNAME)
                    broadcast_message = f'-->[NEW CONNECTION] :: {USERNAME} JOINED THE CHATROOM'
                    broadcast(broadcast_message)

                    msg_to_server = f'-->[NEW CONNECTION] :: {USERNAME} {str(addr)} JOINED'
                    print(msg_to_server)
                    print(f'[ACTIVE CONNECTIONS] :: {threading.activeCount() - 1} \n')

                else:
                    eval_msg = message.split(' ')
                    if eval_msg[2:]==[DISCONNECT_MSG]:
                        connected = False
                    else:
                        # print(message)
                        broadcast(message)
        except:
            connected = False

    try:
        client_index = ALL_CLIENTS.index(client)
        ALL_CLIENTS.remove(ALL_CLIENTS[client_index])
        ALL_USERNAMES.remove(ALL_USERNAMES[client_index])
    except:
        pass

    client.close()
    leaving_msg = f'<--[LEAVING] :: {USERNAME} LEFT THE CHATROOM'
    broadcast(leaving_msg)

    msg_to_server = f'<--[LEAVING] :: {USERNAME} {str(addr)} LEFT'
    print(msg_to_server)
    print(f'[ACTIVE CONNECTIONS] :: {threading.activeCount() - 2}\n')



def start_server():
    global ALL_CLIENTS
    # global ALL_USERNAMES

    IP = socket.gethostbyname(socket.gethostname())
    ADDR = (IP, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print('[STARTING] :: Server is starting...')
    server.listen()
    server_success_message()
    print(f'[LISTENING] :: Server is listening on {IP}\n')

    while True:
        client, addr = server.accept()
        ALL_CLIENTS.append(client)
        thread = threading.Thread(target=handle_client, args=(client,addr))
        thread.start()
        # print(f'[ACTIVE CONNECTIONS] :: {threading.activeCount()-1}')



################################################################################################
#-----------------------------------CLIENT FUNCTIONS-------------------------------------------

def recieve_loop(client):
    while True:
        try:
            receive_message(client)
        except:
            # print('ERROR IN RECIEVING MESSAGE ...')
            client.close()
            break

def send_loop(client,USERNAME):
    while True:
        try:
            msg = f'[{USERNAME}] >> {input("")}'
            send_message(client,msg)
            eval_msg = msg.split(' ')
            if eval_msg[2:]==[DISCONNECT_MSG]:
                goodbye_client_message(USERNAME)
                client.close()
                break
        except:
            print('ERROR IN SENDING MESSAGE...')
            client.close()
            break

def start_client(server_ip):

    IP = server_ip  ## of the server
    ADDR = (IP, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    USERNAME = input('[ENTER USERNAME] :: ')
    send_message(client, USERNAME)

    welcome_client_message(USERNAME)

    recieve_thread = threading.Thread(target=recieve_loop, args=(client,))
    recieve_thread.start()

    send_thread = threading.Thread(target=send_loop, args=(client,USERNAME))
    send_thread.start()




##########-----------MAIN-------------------------------------------------------------------------
## SERVER CODE
# start_server()


## CLIENT CODE
# initialize(port=9999,header=64)
# server_ip = '192.168.10.39'
# start_client(server_ip)
