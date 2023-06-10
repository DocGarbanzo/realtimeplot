import random
import time
from realtimeplot.sender import Sender

# Number of requests to send
num_requests = 1000

# Initialize the data dictionary with keys and initial values
data = {'a': 1.0, 'b': 2.0}
sender = Sender()

# Send multiple requests with random perturbations at a faster rate
for i in range(num_requests):
    # Add random perturbation to the values
    for key in data:
        data[key] += random.uniform(-0.1, 0.1)
    sender.send_data(**data)

    # Wait for a shorter duration
    time.sleep(.02)

# Close the socket
