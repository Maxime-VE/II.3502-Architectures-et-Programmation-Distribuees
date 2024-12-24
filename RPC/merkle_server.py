from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer
from merkle_tree import MerkleTree
import os

LOG_FILE = "logs.txt"
TREE = None

class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def load_logs():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    with open(LOG_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

def save_log(log):
    with open(LOG_FILE, 'a') as f:
        f.write(log + '\n')

def initialize_tree():
    global TREE
    logs = load_logs()
    if logs:
        TREE = MerkleTree(logs)
    else:
        TREE = None

def append_log(log):
    global TREE
    save_log(log)
    if TREE is None:
        TREE = MerkleTree([log])
    else:
        TREE.add_node(log)
    return "Log file has been updated."

def get_root():
    if TREE is None:
        return "No logs are filling the Merkle Tree."
    return TREE.get_root_value()

def get_audit_path(index):
    if TREE is None:
        return "No logs are filling the Merkle Tree."
    try:
        return TREE.gen_path(index)
    except IndexError:
        return "Index out of range."

def get_consistency_path(index):
    if TREE is None:
        return "No logs are filling the Merkle Tree."
    try:
        return TREE.gen_proof(index)
    except IndexError:
        return "Index out of range."


def start_server():
    initialize_tree()
    print("MerkleTree Server is listening on port 5080...")
    with ThreadedXMLRPCServer(("localhost", 5080)) as server:
        server.register_function(append_log, "append_log")
        server.register_function(get_root, "get_root")
        server.register_function(get_audit_path, "get_audit_path")
        server.register_function(get_consistency_path, "get_consistency_path")
        server.serve_forever()

if __name__ == "__main__":
    try:
        start_server()
    except Exception as e:
        print(f"Server Error : {e}")
