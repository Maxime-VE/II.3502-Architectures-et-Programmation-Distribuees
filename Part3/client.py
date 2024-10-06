import threading
import socket

# Neickname selection
nickname = input("Choose a nickname: ")

# Set server connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

# Manage behavior (receive message / disconnect)
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':   # If received code 'NICKNAME' means giving the client's nickname to the server
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured")
            client.close()
            print("You have been disconnected")
            break

# Manage to send a message to a server
def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))

# Start receive Thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Start wrting Thread
write_thread = threading.Thread(target=write)
write_thread.start()