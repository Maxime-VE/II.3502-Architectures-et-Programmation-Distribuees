import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5554   # The port used by the server

# Start connection to server using socket methods
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Infinite Loop of sending/receiving message
while True:
    text = input("What is your message ?  ")
    client.send(text.encode('ascii'))
    message = client.recv(1024)
    print(message)
