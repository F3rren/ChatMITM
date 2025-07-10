# Chat MITM Example - Beta Folder

This project demonstrates a simple client-server chat application with a Man-In-The-Middle (MITM) component for educational purposes. All code and comments are in English.

## Structure

- `Client.py` / `Client2.py`: Client applications that connect to the MITM or server.
- `Server.py` / `Server2.py`: Server applications that receive messages from the client (possibly via MITM).
- `ManInTheMiddle.py` / `ManInTheMiddle2.py`: MITM applications that intercept and optionally modify messages between client and server.
- `key.key`: Example key file (if used for encryption).

## How it works

1. **Client** connects to the MITM (or directly to the server) and sends messages.
2. **MITM** listens for client connections, can modify messages, and forwards them to the server.
3. **Server** receives messages and sends responses back through the MITM to the client.

## Usage

1. Open three terminals (or run in sequence):
   - Start the server: `python Server.py` or `python Server2.py`
   - Start the MITM: `python ManInTheMiddle.py` or `python ManInTheMiddle2.py`
   - Start the client: `python Client.py` or `python Client2.py`

2. Type messages in the client terminal. Type `stop` to terminate the connection.

## Requirements
- Python 3.x
- No external dependencies required

## Notes
- All communication is in plain text for demonstration purposes.
- The MITM can be extended to modify, log, or block messages.
- This project is for educational use only.

## License
Copyright (c) 2025, Created by F3rren - Samuele Alessandro Di Silvestri

This project is for educational purposes.
---

Feel free to modify and experiment with the code to better understand network security concepts!
