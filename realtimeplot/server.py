#!/usr/bin/env python3
import socket
import pickle
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import signal
import sys
from datetime import datetime, timedelta
import argparse


class SerialPyPlotter:
    def __init__(self, host, port, max_records, max_seconds):
        self.host = host
        self.port = int(port)
        self.max_records = int(max_records)
        self.max_seconds = int(max_seconds)

        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific address and port
        self.server_socket.bind((self.host, self.port))

        # Listen for incoming connections
        self.server_socket.listen(1)

        print(f"Server listening on {self.host}:{self.port}")

        # Initialize a dictionary to store the time series data
        self.time_series = {}

        # Initialize the plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')

        # Set dark grey background
        self.fig.set_facecolor('#222222')
        self.ax.set_facecolor('#222222')
        self.ax.tick_params(colors='white')

        # Function to handle graceful shutdown
        def shutdown_server(signal, frame):
            print("Shutting down the server...")
            self.server_socket.close()
            plt.close()
            sys.exit(0)

        # Register the signal handler for Ctrl-C
        signal.signal(signal.SIGINT, shutdown_server)

    def update_time_series(self, data):
        # Update the time series data
        current_time = datetime.now()
        self.x_time_series.append(current_time)

        # Update the time series data for each key-value pair
        for key, value in data.items():
            if key not in self.time_series:
                self.time_series[key] = []

            self.time_series[key].append(value)

            # Remove the oldest data if the length exceeds the maximum records
            if len(self.time_series[key]) > self.max_records:
                self.time_series[key].pop(0)

        return current_time

    def update_plot(self, current_time):
        # Clear the plot
        self.ax.clear()

        # Plot the time series data
        for key, values in self.time_series.items():
            self.ax.plot(self.x_time_series[-len(values):], values, label=key)

        # Calculate x-axis limits
        min_time = current_time - timedelta(seconds=self.max_seconds)
        max_time = current_time

        # Set x-axis limits and format
        self.ax.set_xlim(min_time, max_time)
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        # Set the number of ticks on the x-axis
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(5))

        # Set legend background color
        legend = self.ax.legend()
        legend.get_frame().set_facecolor('#444444')

        # Annotate each data point with its numerical value on the right side of the plot
        for key, values in self.time_series.items():
            last_value = values[-1]
            self.ax.text(max_time, last_value, f"{last_value:.2f}", color='white', va='center')

    def run(self):
        # Create a shared time series for the x-axis
        self.x_time_series = []

        # Create a splash screen with the window name in big letters
        splash_text = self.ax.text(
            0.5, 0.5, 'Serial PyPlotter', fontsize=30, color='white', va='center', ha='center'
        )

        # Set matplotlib window name
        manager = plt.get_current_fig_manager()
        manager.set_window_title('Serial PyPlotter')

        # Display the splash screen immediately
        plt.draw()
        plt.pause(0.1)

        # Flag to track if the first data has been received
        first_data_received = False

        while True:
            # Accept a client connection
            client_socket, addr = self.server_socket.accept()
            print(f"Connection established from: {addr}")

            current_time = datetime.now()

            while True:
                # Receive data from the client
                data = client_socket.recv(4096)

                if not data:
                    break

                # Deserialize the received data
                dictionary = pickle.loads(data)
                print("Received dictionary:", dictionary)

                # Update the time series data
                current_time = self.update_time_series(dictionary)

                if not first_data_received:
                    # Remove the splash screen
                    splash_text.remove()
                    first_data_received = True

                # Update the plot
                self.update_plot(current_time)

                # Refresh the plot
                plt.draw()
                plt.pause(0.001)

                # Send a response to the client
                response = "Dictionary received successfully"
                client_socket.sendall(response.encode())

            # Close the client connection
            client_socket.close()


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Serial PyPlotter')
    parser.add_argument('--host', default='127.0.0.1', help='Server IP address')
    parser.add_argument('--port', default=12345, type=int, help='Server port number')
    parser.add_argument('--max-records', default=200, type=int, help='Maximum number of records to display')
    parser.add_argument('--max-seconds', default=10, type=int, help='Maximum time span to display in seconds')
    args = parser.parse_args()

    # Initialize SerialPyPlotter with provided arguments
    pyplotter = SerialPyPlotter(
        args.host, args.port, args.max_records, args.max_seconds
    )

    # Run the SerialPyPlotter
    pyplotter.run()


if __name__ == '__main__':
    main()
