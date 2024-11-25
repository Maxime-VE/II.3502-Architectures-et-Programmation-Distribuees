import pickle
import random
import socket
import threading
import time

"""
Initialisation of the variables
"""
host = '127.0.0.1'
available_port = range(5000, 5005)  # Available ports

game_values = {}
client_list = {}
for p in available_port:
    client_list[p] = 0
    game_values[p] = 0

port = available_port[0]
connected = False
is_leader = False
leader_connection = None
leader_alive = True
in_election = False
client_socket= None


# Server state information
server_info = {
    "port": None,
    "connected": True,
    "is_leader": False,
    "has_client": False,
    "client_address": None,
    "leader_port": 5000,
    "leader_host": host,
}



"""
Function that contact all server in the range of available ports,
can send different request_type and a message and receive response
"""
def broadcast_qa(request_type="STATE", message=None):
    responses = {}
    request = {"type": request_type, "message": message}

    for other_port in available_port:
        if other_port != port:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.settimeout(0.1)  # Set short timeout to make server set up quicker
                    client.connect((host, other_port))
                    client.sendall(pickle.dumps(request))
                    data = client.recv(16384)
                    response = pickle.loads(data)
                    responses[other_port] = response
            except (socket.error, pickle.PickleError, EOFError) as e:
                responses[other_port] = f"Error: {e}"
    return responses

"""
[LEADER ] Function that check every server to update the client list
"""
def update_client_list():
    global client_list
    responses = broadcast_qa()
    for resp_port, resp_data in responses.items():
        if isinstance(resp_data, dict) and resp_data.get("has_client", False):
            client_list[resp_port] = 1
        else:
            client_list[resp_port] = 0

"""
Function that manage all request comming from client or other servers
and act depending on the request_type.
"""
def handle_client(client, addr):
    global in_election, is_leader, client_socket, leader_connection, leader_alive
    try:
        while True:
            data = client.recv(4096)
            if not data:
                break

            # Deserialize the request
            request = pickle.loads(data)
            request_type = request.get("type")


            if request_type == "ELECTION":
                in_election = True
                response = {"type": "ELECTION_RESPONSE", "port": port}
                client.sendall(pickle.dumps(response))

            if request_type == "NEW_LEADER":
                new_leader_port = request.get("message")
                print(f"New leader announced: port {new_leader_port}")
                server_info["leader_port"] = new_leader_port
                server_info["leader_host"] = host
                is_leader = new_leader_port == port
                in_election = False
                if is_leader:
                    update_client_list()
                    check_and_start_game()


            if not in_election:
                if request_type == "STATE":
                    client.sendall(pickle.dumps(server_info))

                if request_type == "CLIENT_MESSAGE":
                    server_port = request.get("server_port")
                    message = request.get("message")
                    broadcast_to_followers(message, server_port)

                if request_type == "CLIENT":
                    if not server_info["has_client"]:
                        client.sendall(pickle.dumps(server_info))
                        server_info["has_client"] = True
                        server_info["client_address"] = addr
                        client_socket = client
                        print(f"Connected to client {addr}")
                        if not is_leader:
                            leader_connection.sendall(pickle.dumps({"type": "GET_CLIENT","server_port" : port}))
                        else:
                            client_list[port] = 1
                            check_and_start_game()
                    else:
                        client.sendall(pickle.dumps({"error": f"Server already has a client"}))

                if request_type == "MESSAGE":
                    message = request.get("content", "")
                    # DEBUG ZONE
                    if message.lower() == "clients":
                        print(client_list)

                    if message.lower() == "state":
                        print(server_info)

                    if message.lower() == "in_election":
                        print(in_election)

                    print(f"{port}[ME] : {message}")
                    response = {"ack": f"Message received: {message}"}
                    if not server_info["is_leader"]:
                        send_message_to_leader(message, addr)
                    else:
                        broadcast_to_followers(message, port)
                    client.sendall(pickle.dumps(response))

                if request_type == "LEADER_MESSAGE":
                    message = request.get("content", "")
                    server_port = request.get("server_port")
                    print(f"{server_port}: {message}")

                    if server_info["has_client"] and client_socket:
                        try:
                            client_socket.sendall(pickle.dumps({"type": "MESSAGE_FROM_LEADER", "content": f"{server_port} : {message}"}))
                        except Exception as e:
                            print(f"Erreur d'envoi au client: {e}")

                if request_type == "CHOOSE_NUMBER":
                    number_request = {"type": "CHOOSE_NUMBER", "message": "Please choose a number!"}
                    try:
                        client_socket.sendall(
                            pickle.dumps(number_request))
                    except Exception as e:
                        print(f"Erreur d'envoi au client: {e}")

                if request_type == "LOSE_CLIENT":
                    server_port = request.get("server_port")
                    client_list[server_port] = 0

                if request_type == "GET_CLIENT":
                    server_port = request.get("server_port")
                    client_list[server_port] = 1
                    check_and_start_game()

            else:
                client.sendall(pickle.dumps({"error": f"Unknown request type: {request_type}"}))

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        client.close()
        if server_info["client_address"] == addr:
            server_info["has_client"] = False
            server_info["has_client"] = False
            server_info["client_address"] = None
            client_socket = None
            print(f"Closing connection with client {addr}")
            if not server_info["is_leader"]:
                leader_connection.sendall(pickle.dumps({"type": "LOSE_CLIENT","server_port" : port}))
            else:
                client_list[port] = 0


"""
Function that check the number of online client and start Game if more than 3 
"""
def check_and_start_game():
    connected_clients = sum(client_list.values())
    print(f"Currently connected clients: {connected_clients}")

    if connected_clients >= 3:
        print("3 or more clients connected. Starting the game...")
        start_game()

def start_game():
    for player_port in available_port:
        game_values[player_port] = 0
    selected_player = choose_random_client()
    print(f"{selected_player} have been selected")
    if selected_player:
        print("Continue the game ....")
    else:
        print("An error occured. Please get 3 client to start a game.")


"""
Select a player to be the one to start
"""
def choose_random_client():
    connected_ports = [port for port, is_connected in client_list.items() if is_connected == 1]
    if len(connected_ports) > 0:
        return random.choice(connected_ports)
    return None


"""
 Function that keep permanantly a connection with the leader 
"""
def manage_leader_connection():
    global leader_connection, leader_alive
    while not server_info["is_leader"]:
        try:
            leader_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            leader_connection.connect((server_info["leader_host"], server_info["leader_port"]))
            print(f"Connected to leader at {server_info['leader_host']}:{server_info['leader_port']}")
            leader_alive = True
            while leader_alive:
                leader_connection.sendall(pickle.dumps({"type": "HEARTBEAT"})) #Check if leader is still OK
                time.sleep(3)
        except socket.error as e:
            print(f"Error maintaining leader connection: {e}")
            leader_alive = False
            time.sleep(1)
            initiate_leader_election()


""" 
 Function that start an election to choose a new leader when current leader is down.
 THe logic implemented use the lowest server port as the new leader
"""
def initiate_leader_election():
    global is_leader, server_info, in_election
    print("Leader down, starting leader election...")
    in_election = True

    # Run leader election logic (choose the first available server with the lowest port)
    responses = broadcast_qa(request_type="ELECTION")
    potential_leaders = [port]

    for resp_port, resp_data in responses.items():
        if isinstance(resp_data, dict) and resp_data.get("type") == "ELECTION_RESPONSE":
            potential_leaders.append(resp_data["port"])

    new_leader = min(potential_leaders)

    if new_leader == port:
        # This server becomes the leader
        print(f"This server (port {port}) becomes the leader.")
        server_info["is_leader"] = True
        server_info["leader_port"] = port
        is_leader = True

    else:
        # Update the leader information
        print(f"New leader elected on port {new_leader}.")
        server_info["leader_port"] = new_leader
        server_info["leader_host"] = host
        is_leader = False

    broadcast_qa("NEW_LEADER", new_leader)

    in_election = False


"""
Function that echo to leader every message received from a client
"""
def send_message_to_leader(message, addr):
    global leader_connection
    if leader_connection:
        try:
            update = {
                "type": "CLIENT_MESSAGE",
                "message": message,
                "client_address": addr,
                "server_port": server_info["port"]
            }
            leader_connection.sendall(pickle.dumps(update))
        except Exception as e:
            print(f"Error sending message to leader: {e}")
    else:
        print("Leader connection is not available")


"""
[LEADER FUNCTION] Function that send to all follower a message with a request type and a content
"""
def broadcast_to_followers(message, incomming_msg_port=None):
    for follower_port in available_port:
        if follower_port != incomming_msg_port:  # Avoid communication with source server client
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((host, follower_port))
                client_socket.sendall(pickle.dumps({
                    "type": "LEADER_MESSAGE",
                    "content": message,
                    "server_port": incomming_msg_port
                }))
            except Exception as e:
                pass

"""
Function to accept incoming connection in a new Thread
"""
def allow_connection(server):
    while True:
        client, addr = server.accept()
        client_ip, client_port = addr
        # print(f"Connected with {client_ip}:{client_port}") TODO Put it in log file not print

        # Start new Thread
        client_thread = threading.Thread(target=handle_client, args=(client, addr))
        client_thread.start()


"""
 Find an available port to connect 
 Init the context variable
 Start the server
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while not connected:
    try:
        server.bind((host, port))
        server.listen()
        connected = True
    except socket.error as msg:
        port += 1
        if port >= available_port[-1]:  # If no port available, end the process
            print("No port available")
            exit()

# Update server information
server_info["port"] = port

# Check if there is already a leader
responses = broadcast_qa()
leader_found = False
for resp_port, resp_data in responses.items():
    if isinstance(resp_data, dict) and resp_data.get("is_leader", False):
        print(f"Leader found on port {resp_port}")
        leader_found = True
        server_info["leader_port"]= resp_port
        break

# If no leader is found, set the server as
if not leader_found:
    print(f"No leader found. This server (port {port}) becomes the leader")
    is_leader = True
    server_info["is_leader"] = True
    server_info["leader_port"] = port
else:
    print(f"Server (port {port}) is not the leader")

print(f"Server running on port {port}. Leader status: {is_leader}")

# Start the leader communication thread if not leader
if not server_info["is_leader"]:
    leader_thread = threading.Thread(target=manage_leader_connection)
    leader_thread.start()

# Start listening for incoming connections
allow_connection(server)
