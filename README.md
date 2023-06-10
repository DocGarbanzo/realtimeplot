# RealtimePlot

RealtimePlot is a Python package that enables easy plotting of data in real-time. It provides a server-client architecture where you can send data from your Python code to the server, and the server continuously updates and displays the plot based on the received data.

## Features

- Simple and intuitive interface for real-time plotting.
- Client-server architecture for sending and displaying data.
- Interactive plot that updates dynamically as data is received.
- Support for multiple data series and customizable plot appearance.
- Easy integration into existing Python projects.

## Installation

You can install RealtimePlot using pip:

```shell
pip install realtimeplot
```

## Usage

Here's a simple example of how to use RealtimePlot in your Python code:

```Python
import random
import time
from realtimeplot import RealtimePlotClient

# Initialize the RealtimePlot client
client = RealtimePlotClient()

# Start the server (if not already running)
# Make sure to run this command in a separate terminal window
# realtimeplotter

# Generate and send random data
for i in range(200):
    data = {'x': i, 'y': random.random()}
    client.send(data)
    time.sleep(0.05)

# Close the client connection
client.close()
```

Make sure you have the realtimeplot-server command running in a separate terminal window before running the client code.

For more advanced usage and customization options, please refer to the documentation.

## Documentation

For detailed documentation and examples, please visit the RealtimePlot Documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please refer to the Contribution Guidelines for more details.

## Authors

Your Name - Your GitHub Profile

## Acknowledgments

Thanks to the developers of the libraries used in this project.