import os
import socket

HOST = "localhost"
PORT = 5050
FORMAT = "utf-8"
HEADER = 64

def receive_message(conn):
    try:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length.strip())
            return conn.recv(msg_length).decode(FORMAT)
    except Exception as e:
        # [ERROR] An error occurred while receiving the message
        print(f"[ERROR] An error occurred while receiving the message: {e}")
        return ""

def send_message(conn, msg):
    try:     
        # [SERVER] Message received from server: hello from server
        message = "[SERVER] Message received from server: hello from server".encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)
    except Exception as e:
        # [ERROR] An error occurred while sending the message
        print(f"[ERROR] An error occurred while sending the message: {e}")

def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')

clear()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
# [SERVER] Listening on {HOST}:{PORT}...
print(f"[SERVER] Listening on {HOST}:{PORT}...")

while True:
    try:
        conn, addr = server.accept()
        # [CONNECTION] Connection from {addr}
        print(f"[CONNECTION] Connection from {addr}")
        msg = receive_message(conn)
        if msg.lower() == "stop":
            # [SERVER] Received 'stop'. Closing connection.
            print("[SERVER] Received 'stop'. Closing connection.")
            # [SERVER] Connection closed by server.
            send_message(conn, "Connection closed by server.")
            break
        else:
            # [SERVER] Received: {msg}
            print(f"[SERVER] Received: {msg}")
            response = f"Received: {msg}"
            send_message(conn, response)
    except ConnectionAbortedError:
        # [ERROR] An error occurred during the connection
        print("[ERROR] An error occurred during the connection")

# [CONNECTION] Closing the connection
print("[CONNECTION] Closing the connection")
conn.close()
server.close()
