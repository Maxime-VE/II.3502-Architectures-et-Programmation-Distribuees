import pickle
import socket
import time

host = '127.0.0.1'
available_port = range(5000, 5005)  # Available ports

"""
 Function to check the leader state and server availability
"""
def check_server_availability():
    for port in available_port:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(0.5)  # Set timeout for the connection attempt
            client_socket.connect((host, port))

            request = {"type": "CLIENT"}
            client_socket.sendall(pickle.dumps(request))
            data = client_socket.recv(1024)
            response = pickle.loads(data)
            print(response)

            # Check if the server is occupied by another client
            if response.get("has_client", False) or "error" in response:
                print(f"Server on port {port} is currently occupied by another client.")
                client_socket.close()
                continue

            return client_socket, port, response

        except (socket.error, pickle.PickleError, EOFError) as e:
            print(f"Error connecting to port {port}: {e}")
            continue

    return None, None, None

"""
 Function to handle the client interaction with the server
"""
def connect_to_server():
    client_socket, port, server_info = check_server_availability()
    if port is None:
        print("No server available. Exiting...")
        return
    try:
        print(f"Connected to server on port {port}. Leader status: {server_info['is_leader']}")

        while True:
            message = input("Enter a message to send to the server (or 'exit' to disconnect): ")
            if message.lower() == "exit":
                print("Disconnecting from the server...")
                break

            # Send the message to the server
            request = {"type": "MESSAGE", "content": message}
            client_socket.sendall(pickle.dumps(request))

            # Check response from the server
            try:
                data = client_socket.recv(1024)
                response = pickle.loads(data)
                if "ack" in response:
                    print("Received")
                else:
                    print(f"Server response: {response}")
            except socket.timeout:
                print("No response from server (timeout).")
    except (socket.error, pickle.PickleError, EOFError) as e:
        print(f"Connection error: {e}")

    finally:
        client_socket.close()
        print("Connection closed.")


# Main client execution
if __name__ == "__main__":
    connect_to_server()
