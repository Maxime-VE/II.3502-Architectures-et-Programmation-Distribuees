import socket
import threading

HOST = "127.0.0.1"
PORT = 5554

# Fonction qui gère chaque client
def handle_client(conn, addr):
    print(f"Main thread ID: {threading.get_native_id()}")
    print(f"Connected by {addr}")
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                else:
                    print("client : ", data)
            except Exception as e:
                print(f"Error: {e}")
                break
    print(f"Connection with {addr} closed")

# Démarrer le serveur
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            
    except Exception as e:
        print(f"Server stopped due to: {e}")
