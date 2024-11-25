import pickle
import socket
import threading
import time

"""
Initialisation of the variables
"""
host = '127.0.0.1'
available_port = range(5000, 5005)  # Available ports
port = available_port[0]
connected = False
is_leader = False
leader_connection = None
leader_alive = True
in_election = False

# Server state information
server_info = {
    "port": None,
    "connected": True,
    "is_leader": False,
    "has_client": False,
    "client_address": None,
    "leader_port": 5000,
    "leader_host": host
}


"""
Function that contact all server in the range of available ports and can transmit different request_type and a message
"""
def check_leader(request_type="STATE", message=None):
    responses = {}
    request = {"type": request_type, "message": message}

    for other_port in available_port:
        if other_port != port:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                    client.settimeout(0.01)  # Set short timeout to make server set up quicker
                    client.connect((host, other_port))
                    client.sendall(pickle.dumps(request))
                    data = client.recv(1024)
                    response = pickle.loads(data)
                    responses[other_port] = response
            except (socket.error, pickle.PickleError, EOFError) as e:
                responses[other_port] = f"Error: {e}"
    return responses


"""
Function that manage all request comming from client or other servers
and act depending on the request_type.
"""
def handle_client(client, addr):
    global in_election, is_leader
    try:
        while True:
            data = client.recv(1024)
            if not data:
                print(f"Client {addr} disconnected.")
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


            if not in_election:
                if request_type == "STATE":
                    client.sendall(pickle.dumps(server_info))

                if request_type == "CLIENT_MESSAGE":
                    server_port = request.get("server_port")
                    message = request.get("message")
                    print(f"Server {server_port} sent {message}")

                if request_type == "CLIENT":
                    if not server_info["has_client"]:
                        client.sendall(pickle.dumps(server_info))
                        server_info["has_client"] = True
                        server_info["client_address"] = addr
                        print(f"Connected to client {addr}")
                    else:
                        client.sendall(pickle.dumps({"error": f"Server already has a client"}))

                if request_type == "MESSAGE":
                    message = request.get("content", "")
                    print(f"{port}: {message}")
                    response = {"ack": f"Message received: {message}"}
                    if not server_info["is_leader"]:
                        send_message_to_leader(message, addr)
                    client.sendall(pickle.dumps(response))

            else:
                client.sendall(pickle.dumps({"error": f"Unknown request type: {request_type}"}))

    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        client.close()
        if server_info["client_address"] == addr:
            server_info["has_client"] = False
            server_info["client_address"] = None
            print(f"Closing connection with client {addr}")


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
            time.sleep(3)
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
    responses = check_leader(request_type="ELECTION")
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

    check_leader("NEW_LEADER", new_leader)

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
Function to accept incoming connection in a new Thread
"""
def allow_connection(server):
    while True:
        client, addr = server.accept()
        client_ip, client_port = addr
        print(f"Connected with {client_ip}:{client_port}")

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
responses = check_leader()
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
