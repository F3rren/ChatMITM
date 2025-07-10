import os
import socket

HOST = "localhost"
SERVER_PORT = 5050

ATTACKER_PORT = 65432  # Port on which the attacker listens
FORMAT = "utf-8"  # Message encoding format
HEADER = 64  # Header length for communication

# Creates a socket for the attacker to listen for client connections
attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
attacker_socket.bind((HOST, ATTACKER_PORT))
attacker_socket.listen()  # Listens for one connection at a time

# Creates a socket to connect to the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, SERVER_PORT))


def modify_msg(msg):
    # Modify the message received from the client
    new_msg = input("[INFO] Write the message to modify: ")
    altered_msg = msg.replace(msg, new_msg)
    return altered_msg


def sendToServer(msg):
    try:
        # [INFO] MITM Sending response to server...
        print("[INFO] MITM Sending response to server...")
        decrypted_msg = msg  # Encrypt the message
        msg_length = len(decrypted_msg)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Padding
        server_socket.send(send_length)
        server_socket.send(decrypted_msg)
    except Exception as e:
        # [ERROR] An error occurred while sending the message from MITM
        print(f"[ERROR] An error occurred while sending the message from MITM: {e}")


def receiveFromServer():
    msg = server_socket.recv(HEADER).decode(FORMAT)
    if not msg:
        # [INFO] Connection closed by server.
        print("[INFO] Connection closed by server.")
    try:
        # [MESSAGE] Received from server: {msg}
        print(f"[MESSAGE] Received from server: {msg}")
    except Exception as e:
        # [ERROR] Error while receiving the message from the server
        print(f"[ERROR] Error while receiving the message from the server: {e}")


def sendToMitm(msg):
    try:
        # [INFO] MITM Sending message to client...
        print("[INFO] MITM Sending message to client...")
        attacker_socket.send(msg)
    except Exception as e:
        # [ERROR] An error occurred while sending the message to the client
        print(f"[ERROR] An error occurred while sending the message to the client: {e}")


def listen():
    while True:
        # Accepts the connection from the client (which connects to the attacker)
        conn, addr = attacker_socket.accept()
        # [INFO] Connection established with client: {addr}
        print(f"[INFO] Connection established with client: {addr}")
        try:
            while True:
                # Receives the length of the message to decode
                client_msg_len = conn.recv(HEADER).decode(FORMAT)
                if not client_msg_len:
                    # [INFO] Connection closed by client.
                    print("[INFO] Connection closed by client.")
                    break
                # Receives the full encrypted message
                msg = conn.recv(HEADER).decode(FORMAT)
                # Modify the message received from the client
                # altered_msg = modify_msg(msg)
                altered_msg = msg  # For now does not modify the message, just sends it to the server
                # [MESSAGE] Manipulated response: {altered_msg}
                print(f"[MESSAGE] Manipulated response: {altered_msg}")
                # Sends the manipulated message to the server
                print(f"[INFO] Sending the manipulated message to the server...")
                sendToServer(altered_msg.encode(FORMAT))
                # If the message is "stop", end communication with the client
                if msg == "stop":
                    # [INFO] Received 'stop' message. Closing connection with client.
                    print("[INFO] Received 'stop' message. Closing connection with client.")
                    conn.send(b"Connection closed.")
                    conn.close()
                    break  # Exits the inner loop and attacker keeps listening for new connections
                receiveFromServer()
        except Exception as e:
            # [ERROR] An error occurred
            print(f"[ERROR] An error occurred: {e}")
            conn.close()
            server_socket.close()
            continue


def start_mitm():
    # [INFO] Listening on port {ATTACKER_PORT}...
    print(f"[INFO] Listening on port {ATTACKER_PORT}...")
    try:
        while True:
            listen()  # After the connection is closed, the server keeps listening for new connections
    except KeyboardInterrupt:
        # [INFO] Manual interruption detected. Closing connections...
        print("[INFO] Manual interruption detected. Closing connections...")
    finally:
        # Closes all connections when the outer loop ends
        if attacker_socket:
            attacker_socket.close()
        if server_socket:
            server_socket.close()
        # [INFO] Connections closed. Program terminated.
        print("[INFO] Connections closed. Program terminated.")
    attacker_socket.close()
    server_socket.close()


def clear():
    return os.system('cls')
clear()
start_mitm()
