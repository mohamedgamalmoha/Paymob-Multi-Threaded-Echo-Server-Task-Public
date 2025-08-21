import socket

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 65432
BUFFER_SIZE = 1024


class EchoClient:
    """
    A simple echo client that connects to an echo server,
    """

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        """
        Initialize the EchoClient with host and port.

        Args:
            - host (str): Host address of the echo server
            - port (int): Port number of the echo server
        """
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to the echo server.

        Returns:
            - bool: True if connection was successful, False otherwise
        """
        try:
            # Create IPv4 TCP socket
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server
            self.client_socket.connect((self.host, self.port))
            self.connected = True

            print(f"Connected to echo server at {self.host}:{self.port}")
            print("Type 'exit' to quit the client")
            print("-" * 40)

            return True

        except ConnectionRefusedError:
            print(f"Error: Could not connect to server at {self.host}:{self.port}")
            print("Make sure the server is running.")
            return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send_message(self, message: str) -> None:
        """
        Send a message to the server and receive the echo.

        Args:
            - message: String message to send

        Returns:
            - String response from server, or None if error occurred
        """
        try:
            # Send message to server
            self.client_socket.send(message.encode('utf-8'))

            # Receive echoed response
            response = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
            return response

        except ConnectionResetError:
            print("\nError: Server closed the connection unexpectedly")
            return None
        except Exception as e:
            print(f"\nError sending message: {e}")
            return None

    def run(self) -> None:
        """
        Main client loop for user interaction.
        """
        if not self.connect():
            return

        try:
            while self.connected:
                # Get user input
                try:
                    user_input = input("Enter message: ").strip()
                except (EOFError, KeyboardInterrupt):
                    # Handle Ctrl+C or Ctrl+D
                    print("\nExiting...")
                    user_input = "exit"

                if not user_input:
                    # Skip empty messages
                    continue

                # Send message and get response
                response = self.send_message(user_input)

                if response is None:
                    # Error occurred, break out of loop
                    break

                # Check if we're exiting
                if user_input.lower() == 'exit':
                    print(f"Server response: {response}")
                    print("Disconnected from server")
                    break

                # Display server's echo
                print(f"Server echo: {response}")

        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            self.disconnect()

    def disconnect(self) -> None:
        """
        Close the connection to the server.
        """
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass  # Ignore errors during cleanup
        self.connected = False


def main():
    """
    Main function to start the echo client.
    """
    print("Echo Client")
    print("=" * 20)

    client = EchoClient()
    client.run()


if __name__ == "__main__":
    main()
