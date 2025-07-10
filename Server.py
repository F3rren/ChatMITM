
import socket
import threading
import os

SERVER = "localhost"  # Server IP address
HEADER = 64  # Header length for communication
FORMAT = "utf-8"  # Message encoding format
ADDR = (SERVER, 5050) # Defines the server address and port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a socket for the server
server.bind(ADDR) # Binds the socket to the address and port

def sendToMitm(conn):
    # [INFO] Sending response to client...
    print("[INFO] Sending response to client...")
    message = "Response from server".encode(FORMAT)  # Message to send to the client
    conn.send(message)

# Function to handle connection with a client
def handle_client(conn, addr):
    # [NEW CONNECTION] {addr} connected.
    print(f"(!)[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            # Receives the message length
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                # Converts the message length to integer
                msg_length = int(msg_length)
                # Receives the encrypted message
                msg = conn.recv(msg_length).decode(FORMAT)
                # Decrypts the message
                print(f"[MESSAGE]: {msg} from user {addr}")  # Prints the decrypted message
                # If the message is "stop", close the connection
                if msg == "stop":
                    # [CLOSING] Closing connection with {addr}
                    print("[CLOSING] Closing connection with", addr)
                    conn.send("Connection closed".encode())
                elif msg is None:
                    # [ERROR] Invalid message length.
                    print("[ERROR] Invalid message length.")
                    break
                sendToMitm(conn)
        except Exception as e:
            # [ERROR] Error while receiving the message
            print(f"[ERROR] Error while receiving the message: {e}")
            break
    # Closes the connection with the client
    conn.close()
    # [DISCONNECTION] {addr} disconnected.
    print(f"[DISCONNECTION] {addr} disconnected.")

# Function to start the server
def start():
    # Puts the server in listening mode
    server.listen()
    # [INFO] Server is listening on {SERVER}
    print(f"[INFO] Server is listening on {SERVER}")
    # Infinite loop to keep the server running
    while True:
        # Accepts a new connection from a client
        conn, addr = server.accept()
        # Creates a new thread to handle the client connection
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        # Starts the thread
        thread.start()
        # Prints the number of active connections (excluding the main thread)
        print(f"[INFO] Active connections: {threading.active_count() - 1}")

# Server startup message
def clear():
    return os.system('cls')
clear()
print("The server is starting...")
# Start the server
start()
