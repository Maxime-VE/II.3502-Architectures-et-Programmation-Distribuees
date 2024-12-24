import xmlrpc.client


def run():
    print("Trying to connect to RPC server...")
    try:
        with xmlrpc.client.ServerProxy("http://localhost:5080/") as proxy:
            print("Connected to LogServer")

            while True:
                print("\nAvailable options :")
                print("1. Add a log")
                print("2. Get hash root")
                print("3. Get audit path (genPath())")
                print("4. Get consistency proof (genProof())")
                print("5. Quit")

                choix = input("Select an option (1-5) : ").strip()

                if choix == "1":
                    log = input("Enter the log to add : ").strip()
                    if log:
                        response = proxy.append_log(log)
                        print(f"Server answer : {response}")
                    else:
                        print("Log must not be empty.")

                elif choix == "2":
                    root_hash = proxy.get_root()
                    print(f"Current HashRoot : {root_hash}")

                elif choix == "3":
                    try:
                        index = int(input("Enter index for audit path ").strip())
                        audit_path = proxy.get_audit_path(index)
                        if isinstance(audit_path, list):
                            print(f"Audit Path : {[node[0] for node in audit_path]}")
                        else:
                            print(f"Error : {audit_path}")
                    except ValueError:
                        print("Index is not valid.")

                elif choix == "4":
                    try:
                        index = int(input("Enter index for consistency path proof: ").strip())
                        consistency_path = proxy.get_consistency_path(index)
                        if isinstance(consistency_path, list):
                            print(f"Path : {consistency_path}")
                        else:
                            print(f"Erreur : {consistency_path}")
                    except ValueError:
                        print("Index is not valid.")

                elif choix == "5":
                    print("Client disconnected.")
                    break

                else:
                    print("Incorrect option. Select an option (1-5).")
    except ConnectionRefusedError:
        print("Server unavailable. Check that the server is up and running.")
    except Exception as e:
        print(f"Unexpected Error : {e}")


if __name__ == "__main__":
    run()
