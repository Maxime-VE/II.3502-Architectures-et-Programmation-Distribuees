import socket


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5555   # The port used by the server

# Define where the server has to listen connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

client, address = server.accept()
print(f"Connected with {address}")

# User is now connected
# We just send back its message here
while True:
    data = client.recv(1024)
    if not data:
        break
    client.send(data)