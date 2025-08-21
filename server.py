import socket
import logging
import threading


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Server configuration
HOST = '127.0.0.1'  # localhost
PORT = 65432
BUFFER_SIZE = 1024


class EchoServer:
    """
    A simple echo server that listens for incoming TCP connections,
    receives messages from clients, and echoes them back.
    """

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        """
        Initialize the EchoServer with host and port.

        Args:
            - host (str): Host address to bind the server to
            - port (int): Port number to listen on
        """
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def handle_client(self, client_socket: socket.socket, client_address:tuple[str, int]) -> None:
        """
        Handle communication with a single client in a separate thread.

        Args:
            - client_socket: Socket object for the client connection
            - client_address: Tuple containing client IP and port
        """
        client_ip, client_port = client_address
        logging.info(f"New client connected: {client_ip}:{client_port}")

        try:
            while True:
                # Receive message from client
                message = client_socket.recv(BUFFER_SIZE).decode('utf-8')

                if not message:
                    # Client disconnected unexpectedly
                    logging.info(f"Client {client_ip}:{client_port} disconnected unexpectedly")
                    break

                logging.info(f"Received from {client_ip}:{client_port}: '{message}'")

                # Check if client wants to exit
                if message.lower().strip() == 'exit':
                    logging.info(f"Client {client_ip}:{client_port} requested to exit")
                    # Send acknowledgment before closing
                    client_socket.send("Goodbye!".encode('utf-8'))
                    break

                # Echo the message back to client
                client_socket.send(message.encode('utf-8'))
                logging.info(f"Echoed to {client_ip}:{client_port}: '{message}'")

        except ConnectionResetError:
            logging.info(f"Client {client_ip}:{client_port} forcibly closed connection")
        except Exception as e:
            logging.error(f"Error handling client {client_ip}:{client_port}: {e}")
        finally:
            # Clean up client connection
            client_socket.close()
            logging.info(f"Connection with {client_ip}:{client_port} closed")

    def start(self) -> None:
        """
        Start the echo server and listen for incoming connections.
        This method runs in the main thread and spawns a new thread for each client connection.
        """

        try:
            # Create IPv4 TCP socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Allow reusing the address (helpful for quick restarts)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind to host and port
            self.server_socket.bind((self.host, self.port))

            # Start listening for connections (max 5 pending connections)
            self.server_socket.listen(5)
            self.running = True

            logging.info(f"Echo server started on {self.host}:{self.port}")
            logging.info("Waiting for client connections...")

            while self.running:
                try:
                    # Accept incoming connection
                    client_socket, client_address = self.server_socket.accept()

                    # Create and start new thread for this client
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True  # Thread will exit when main program exits
                    )
                    client_thread.start()

                except OSError:
                    # Socket was closed, likely during shutdown
                    if self.running:
                        logging.error("Socket error occurred")
                    break

        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            self.shutdown()

    def shutdown(self) -> None:
        """
        Gracefully shutdown the server.
        """
        logging.info("Shutting down server...")
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logging.info("Server shutdown complete")


def main():
    """
    Main function to start the echo server.
    """

    server = EchoServer()

    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server interrupted by user (Ctrl+C)")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
