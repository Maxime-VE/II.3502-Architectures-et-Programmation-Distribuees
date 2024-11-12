import threading
import socket

host = '127.0.0.1' # Localhost
available_port = range(5000, 5005)
port = available_port[0]
connected = False

# Define the server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not connected:
    print(f'Port {port}')
    try:
        server.bind((host, port))
        server.listen()
        connected = True
    except socket.error as msg:
        port = port + 1

    if port == available_port[len(available_port) - 1]:
        print("No port available")
        exit()


clients = [] # List of clients
nicknames = [] # Names of clients

# Send message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# End a connection with a client
def disconnect(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    broadcast(f"{nickname} left the chat".encode('ascii'))
    print(f"{nickname} disconnected".encode('ascii'))
    nicknames.remove(nickname)

# Manage behavior (broadcast or disconnect)
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            disconnect(client)
            break

# Manage new connection
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with { str(address)}") # Show in server console address of the new client

        client.send('NICKNAME'.encode('ascii')) # First contact get the client Nickname
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"The Nickname of the client is {nickname}")
        broadcast(f" {nickname} joined the chat !".encode('ascii')) # Announce new client in chat
        client.send('Connected to the chat !'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,)) # Start a new thread
        thread.start()

print('Server is listening...')
receive()

