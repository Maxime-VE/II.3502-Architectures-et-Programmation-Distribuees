import pickle
import socket

host = '127.0.0.1' # Localhost
available_port = range(5000, 5005)
leader_port = 5000
port = available_port[0]
connected = False
is_leader = False
clients = [] # List of clients
nicknames = [] # Names of clients

# Define the server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not connected:
    try:
        server.bind((host, port))
        server.listen()
        connected = True
    except socket.error as msg:
        port = port + 1
        if port == available_port[len(available_port) - 1]:
            print("No port available")
            exit()

if port == leader_port:
    is_leader = True


# Send message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle request from a client
def handle_write_request(data):
    print(f"Received write request: {data}")
    if is_leader:
        # Simulate leader logic for assigning proposal tag (sequence number, epoch)
        proposal_tag = {'sequence': 1, 'epoch': 1}
        print(f"Leader processing Write request with proposal tag: {proposal_tag}")
        # Send proposal to followers
        for client in clients:
            client.send(pickle.dumps(proposal_tag))  # send proposal tag to clients
        return proposal_tag
    else:
        print("Forwarding write request to leader...")
        # Forward the request to the leader
        leader_client = clients[0]  # Assume leader is the first client for simplicity
        leader_client.send(pickle.dumps(data))
        return None

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                data = pickle.loads(message)  # Unpickle the received message
                if data['type'] == 'Write':
                    handle_write_request(data['data'])
                else:
                    print(f"Unknown message type: {data['type']}")
            else:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    client.close()


# Manage new connection
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}") # Show in server console address of the new client
        clients.append(client)
        nickname = str(address)[-2:]
        nicknames.append(nickname)

        client.send('Connected to the game !'.encode('ascii'))
        broadcast(f" {nickname} joined the game !".encode('ascii')) # Announce new client in chat
        handle_client(client)

print('Server is listening...')
receive()

