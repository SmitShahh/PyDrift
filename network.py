import socket
import pickle

server = "127.0.0.1"

class Network:
    def __init__(self):
        # Create a client socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = 3485
        self.addr = (self.server, self.port)
        self.pos = None
        
        # Attempt to connect and set the initial position
        self.connect()

    def getPos(self):
        """Return the last received position."""
        return self.pos

    def connect(self):
        try:
            # Connect to the server
            self.client.connect(self.addr)
            
            # Receive initial data from the server
            data = self.client.recv(1000)
            
            if data:
                self.pos = pickle.loads(data)
            else:
                print("No data received from the server.")
        except Exception as e:
            print(f"Connection error: {e}")

    def send(self, data):
        try:
            # Send data to the server
            self.client.send(pickle.dumps(data))
            
            # Receive response from the server
            response = self.client.recv(1000)
            
            if response:
                return pickle.loads(response)
            else:
                print("No response received from the server.")
                return None
        except socket.error as e:
            print(f"Socket error: {e}")
        except pickle.PickleError as e:
            print(f"Pickle error: {e}")
        return None