import os
import socket

HOST = "localhost"
SERVER_PORT = 5050

ATTACKER_PORT = 65432
FORMAT = "utf-8"
HEADER = 64

# Socket to listen for the client
attacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
attacker_socket.bind((HOST, ATTACKER_PORT))
attacker_socket.listen()

# Socket to connect to the real server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect((HOST, SERVER_PORT))



def modify_msg(msg):
    # Asks the attacker to modify the message
    new_msg = input(
        f"[MODIFY] Message received: '{msg}'\nWrite the new message (or leave empty/press enter to not modify): "
    )
    if new_msg.strip():
        return new_msg
    return msg



def send_message(sock, msg):
    try:
        # [INFO] Sending message: {msg}
        print(f"[INFO] Sending message: {msg}")
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b" " * (HEADER - len(send_length))
        sock.send(send_length)
        sock.send(message)
    except Exception as e:
        # [ERROR] An error occurred while sending the message
        print(f"[ERROR] An error occurred while sending the message: {e}")



def receive_message(sock):
    try:
        msg_length = sock.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length.strip())
            return sock.recv(msg_length).decode(FORMAT)
        return ""
    except Exception as e:
        # [ERROR] An error occurred while receiving the message
        print(
            f"[ERROR] An error occurred while receiving the message: {e}"
        )
        return ""



def listen():
    conn, addr = attacker_socket.accept()
    # [CONNECTION] Client connected from {addr}
    print(f"[CONNECTION] Client connected from {addr}")
    while True:
        try:
            # Receives message from client
            client_msg = receive_message(conn)
            if not client_msg:
                # [INFO] No message received. Closing.
                print("[INFO] No message received. Closing.")
                break
            if client_msg.lower() == "stop":
                # [INFO] Stop message received. Closing connection.
                print("[INFO] Stop message received. Closing connection.")
                send_message(conn, "Connection closed by MITM.")
                break
            # Optionally modify the message
            altered_msg = modify_msg(client_msg)
            # Send the message to the server
            send_message(server_socket, altered_msg)
            # Receive response from server
            server_response = receive_message(server_socket)
            # Forward the response to the client
            # print(f"[MITM → CLIENT] Sending: {server_response}")
            send_message(conn, server_response)
        except Exception as e:
            # [ERROR] An error occurred
            print(f"[ERROR] An error occurred: {e}")
            break
    conn.close()
    # [INFO] Connection with client closed.
    print("[INFO] Connection with client closed.")


def clear():
    return os.system("cls" if os.name == "nt" else "clear")


def start_mitm():
    clear()
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


start_mitm()
