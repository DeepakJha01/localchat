
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

def receive_loop(client):
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

    recieve_thread = threading.Thread(target=receive_loop, args=(client,))
    recieve_thread.start()

    send_thread = threading.Thread(target=send_loop, args=(client,USERNAME))
    send_thread.start()


#------------------HELP--------------------------------------------------------------------------
def help():
    print('\nlocalchat :: python library for quickly writing server and client side programs for a Chat Group on LAN')
    print('Follow the below instructions to use this library')

    print("""
    Localchat library is pre-initialized with the following values of the GLOBAL variables
    PORT (port number) = 9999,                    FORMAT (encoding format) = 'utf-8'
    DISCONNECT_MSG (client disconnects on typing this message) = '!CONNECT'     
    HEADER (buffer size to send the size of the message) = 64
    
    1. initialize(port,format,header,disconnect_msg)    -   to change any of the pre-initialized global variables
                                                            (should be same for server and client)
                                                            
    2. start_server()   -   binds the server with its (IP, PORT) and gets ready to accept multiple clients requests,
                            receive messages and broadcast the messages to all the client available
    
    3. start_client(server_ip)   -   connects the client with the server ipv4 address provided and gets ready to send
                                     and receive messages concurrently
    
    4. send_message(client, message)   -    server can send the message to the client OR
                                            client can send message to the connected server       
    
    5. receive_msg(client)  -   server can receive message from the client OR
                                client can receive message from the connected server
    
    6. broadcast(message)   -   server broadcasts the message to all the available clients(ALL_CLIENTS)
    
    Will be adding new features soon ...
    """)
#-------------------------------------------------------------------------------------------------------------------



##########-----------MAIN-------------------------------------------------------------------------
## SERVER CODE
# start_server()


## CLIENT CODE
# initialize()
# server_ip = '111.111.11.11'
# start_client(server_ip)
