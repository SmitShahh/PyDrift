import socket
from _thread import *
import pickle
import sys

server = "127.0.0.1"  # Ensure this matches the client address
port = 3485
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(f"Binding error: {e}")
    sys.exit()

s.listen(2)
print("Waiting for a connection, Server Started")

players = [[True, 1300, 700, 270, False, 0], [False, 1400, 800, 270, False, 0]]

def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    while True:
        try:
            data = pickle.loads(conn.recv(1000))
            if not data:
                print("Disconnected")
                break
            else:
                players[player] = data
                reply = players[1 - player]
                print("Received: ", data)
                print("Sending : ", reply)
                conn.sendall(pickle.dumps(reply))
        except Exception as e:
            print(f"Thread error: {e}")
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer = (currentPlayer + 1) % 2  # Toggle between 0 and 1
