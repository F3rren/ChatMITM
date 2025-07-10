import socket, os


# Definition of constants
HEADER = 64  # Header length for communication
SERVER_PORT = 5050  # Port used for connection
FORMAT = "utf-8"  # Message encoding format
SERVER = "localhost"  # Server IP address
CLIENT_PORT = 65432  # Port on which the attacker listens
ADDR = (SERVER, CLIENT_PORT)  # Tuple representing the server address


# Create the client socket and connect to the server
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(ADDR)
    # [INFO] Connection to server {SERVER} on port {SERVER_PORT} successful. Ready to send messages.
    print(f"[INFO] Connection to server {SERVER} on port {SERVER_PORT} successful. Ready to send messages.")
    # Generation of an encryption key
except ConnectionRefusedError:
    # Error: unable to connect to the server. Check that the server is running and the address is correct.
    print("Error: unable to connect to the server. Check that the server is running and the address is correct.")
    exit()
except socket.error as e:
    # Connection error
    print(f"Connection error: {e}")
    exit()



# Function to send a message to the server
def sendToMitm(msg):
    # Encode the message
    message = msg.encode(FORMAT)
    # Calculate the length of the message
    msg_length = len(message)
    # Create the header with the message length
    send_lenght = str(msg_length).encode(FORMAT)
    send_lenght += b' ' * (HEADER - len(send_lenght))
    # Send the header and the message to the server
    client.send(send_lenght)
    client.send(message)



def receiveFromMitm():
    msg = client.recv(HEADER).decode(FORMAT)
    if not msg:
        # [INFO] Connection closed by server.
        print("[INFO] Connection closed by server.")
    try:
        # [MESSAGE] Received from server: {msg}
        print(f"[MESSAGE] Received from server: {msg}")
    except Exception as e:
        # [ERROR] Error while receiving the message from the server
        print(f"[ERROR] Error while receiving the message from the server: {e}")


def clear():
    return os.system('cls')
clear()
while True:
    msg = input("Enter the message to send (type 'stop' to terminate): ")
    # Check if the user wants to terminate
    if msg.lower() == "stop" or msg.upper() == "STOP":
        print("Connection terminated.")
        break
    else: 
        # Encrypt and send the message
        sendToMitm(msg)
        print("hello")
        # If the message was sent successfully, receive the response from the server
        data = client.recv(1024).decode()
        print(f"Response from server: {data}")
        