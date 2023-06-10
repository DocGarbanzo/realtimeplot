import socket
import pickle
from realtimeplot import HOST, PORT


class Sender:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the server
        try:
            self.client_socket.connect((self.host, self.port))
        except Exception as e:
            print(f'Failed to connect to {self.host}:{self.port}: {e}')
            raise

    def send_data(self, *args, **kwargs):
        data = None
        if args:
            assert not kwargs, \
                "Can only send list of arguments or key/values but not both"
            data = {f'arg_{i}': arg for i, arg in enumerate(args)}
        else:
            data = kwargs

        # Serialize the dictionary
        serialized_data = pickle.dumps(data)

        # Send the data to the server
        self.client_socket.sendall(serialized_data)
        # Receive a response from the server
        response = self.client_socket.recv(4096).decode()
        if response != "OK":
            print(f"Problem - response from server: {response}")
