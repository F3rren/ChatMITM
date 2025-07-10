
import os
import socket

HOST = "localhost"
PORT = 65432  # Talks to the attacker (MITM)
FORMAT = "utf-8"
HEADER = 64

def initialize():
    def clear():
        return os.system('cls')
    clear()
    try:
        # [INFO] Initializing client...
        print("[INFO] Initializing client...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        # [CLIENT] Connected. Write messages to send to the server through MITM.
        print("[CLIENT] Connected. Write messages to send to the server through MITM.")
        # [INFO] Type 'stop' to close the connection.
        print("[INFO] Type 'stop' to close the connection.\n")
    except Exception as e:
        # [ERROR] An error occurred during client initialization
        print(f"[ERROR] An error occurred during client initialization: {e}")
        return None
    return client

def send_message(sock, msg):
    try:
        # [INFO] Sending message: {msg}
        print(f"[INFO] Sending message: {msg}")
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        sock.send(send_length)
        sock.send(message)
    except Exception as e:
        # [ERROR] An error occurred while sending the message
        print(f"[ERROR] An error occurred while sending the message: {e}")

def receive_message(sock):
    msg_length = sock.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length.strip())
        return sock.recv(msg_length).decode(FORMAT)
    return ""

client = initialize()
if client:
    while True:
        try:
            msg = input("[MESSAGE] Enter message: ")
            send_message(client, msg)
            response = receive_message(client)
            print(f"{response}")
            if msg.lower() == "stop":
                break
        except Exception as e:
            # [ERROR] An error occurred
            print(f"[ERROR] An error occurred: {e}")
            break
    client.close()
