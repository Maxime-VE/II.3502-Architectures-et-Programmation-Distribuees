import socket
import pickle

# Client setup
nickname = input("Choose a nickname: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))

def receive():
    """ Listen for messages from the server. """
    while True:
        try:
            message = client.recv(1024)
            if message:
                data = pickle.loads(message)  # Unpickle the received data
                print(f"Received from server: {data}")
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def send_write_request(value):
    """ Send a Write request to the server. """
    write_request = {'type': 'Write', 'data': value}
    client.send(pickle.dumps(write_request))

# Main loop for client interaction
def main():
    # Start receiving data
    receive()

    # Client main interaction loop
    while True:
        action = input("Do you want to make a Write request? (y/n): ")
        if action == 'y':
            value = int(input("Enter a number (0-100): "))
            send_write_request(value)
        else:
            print("Exiting client.")
            break

if __name__ == "__main__":
    main()
