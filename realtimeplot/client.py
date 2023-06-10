import socket
import pickle
import random
import time

# Server configuration
host = '127.0.0.1'  # Enter your server IP address here
port = 12345  # Enter the server port number

# Number of requests to send
num_requests = 1000

# Initialize the data dictionary with keys and initial values
data = {'a': 1.0, 'b': 2.0}

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

# Send multiple requests with random perturbations at a faster rate
for i in range(num_requests):
    # Add random perturbation to the values
    for key in data:
        data[key] += random.uniform(-0.1, 0.1)

    # Serialize the dictionary
    serialized_data = pickle.dumps(data)

    # Send the data to the server
    client_socket.sendall(serialized_data)

    # Receive a response from the server
    response = client_socket.recv(4096)
    print(f"Request {i+1} - Response from server: {response.decode()}")

    # Wait for a shorter duration
    time.sleep(.05)

# Close the socket
