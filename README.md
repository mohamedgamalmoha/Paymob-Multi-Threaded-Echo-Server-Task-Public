# Paymob-Multi-Threaded-Echo-Server-Task-Public

A simple yet robust implementation of a multi-threaded echo server and client in Python using IPv4 socket communication.

## 📋 Overview

This project demonstrates fundamental network programming concepts including:
- IPv4 TCP socket communication
- Multi-threaded server architecture
- Client-server message exchange
- Graceful connection handling
- Comprehensive logging

The server can handle multiple concurrent client connections, with each client running in its own thread. Messages are echoed back to clients until they send the 'exit' command.

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────────────┐
│   Client 1  │◄────────┤                     │
├─────────────┤         │                     │
│   Client 2  │◄────────┤   Echo Server       │
├─────────────┤         │   (Multi-threaded)  │
│   Client 3  │◄────────┤                     │
└─────────────┘         └─────────────────────┘
     TCP/IPv4                 127.0.0.1:65432
```

## 📁 Project Structure

```
echo-server/
├── server.py          # Multi-threaded echo server
├── client.py          # Echo client
└── README.md          # This file
```

## ⚡ Quick Start

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

### Running the Application

1. **Clone or download the project files**

2. **Start the server:**
   ```bash
   python server.py
   ```
   
   You should see output like:
   ```
   2024-01-15 10:30:45 - INFO - Echo server started on 127.0.0.1:65432
   2024-01-15 10:30:45 - INFO - Waiting for client connections...
   ```

3. **Run the client (in a new terminal):**
   ```bash
   python client.py
   ```
   
   You should see:
   ```
   Echo Client
   ====================
   Connected to echo server at 127.0.0.1:65432
   Type 'exit' to quit the client
   ----------------------------------------
   Enter message: 
   ```

4. **Test the echo functionality:**
   - Type any message and press Enter
   - The server will echo it back
   - Type 'exit' to disconnect

## 🚀 Features

### Server (server.py)

#### Core Functionality
- **IPv4 TCP Sockets**: Uses `socket.AF_INET` and `socket.SOCK_STREAM`
- **Multi-threading**: Each client connection handled in separate thread
- **Concurrent Connections**: Supports multiple simultaneous clients
- **Echo Service**: Mirrors all client messages back to sender

#### Advanced Features
- **Graceful Shutdown**: Proper cleanup with Ctrl+C
- **Socket Reuse**: `SO_REUSEADDR` option for quick restarts
- **Connection Monitoring**: Real-time logging of all network activity
- **Error Handling**: Robust handling of unexpected disconnections

#### Logging
- Client connections and disconnections with IP addresses
- All messages received and sent
- Timestamped log entries
- Error tracking and reporting

### Client (client.py)

#### User Interface
- **Interactive CLI**: Simple command-line interface
- **Real-time Feedback**: Immediate display of server responses
- **Clean Exit**: Graceful disconnection with 'exit' command
- **Error Messages**: Clear feedback for connection issues

#### Features
- **Automatic Connection**: Connects to localhost:65432 on startup
- **Message Validation**: Skips empty messages
- **Interrupt Handling**: Supports Ctrl+C and Ctrl+D for exit
- **Connection Status**: Clear indication of connection state

## 🧪 Testing Multi-threading

To verify the server handles multiple concurrent connections:

1. **Start the server:**
   ```bash
   python server.py
   ```

2. **Open multiple terminals and run clients:**
   ```bash
   # Terminal 1
   python client.py
   
   # Terminal 2  
   python client.py
   
   # Terminal 3
   python client.py
   ```

3. **Send messages from different clients** and observe the server logs showing concurrent handling

4. **Example server output:**
   ```
   2024-01-15 10:31:15 - INFO - New client connected: 127.0.0.1:54321
   2024-01-15 10:31:20 - INFO - New client connected: 127.0.0.1:54322
   2024-01-15 10:31:25 - INFO - Received from 127.0.0.1:54321: 'Hello from client 1'
   2024-01-15 10:31:25 - INFO - Echoed to 127.0.0.1:54321: 'Hello from client 1'
   2024-01-15 10:31:30 - INFO - Received from 127.0.0.1:54322: 'Hello from client 2'
   2024-01-15 10:31:30 - INFO - Echoed to 127.0.0.1:54322: 'Hello from client 2'
   ```

## 🔧 Configuration

Both server and client use these default settings:

```python
HOST = '127.0.0.1'  # localhost
PORT = 65432        # Server port
BUFFER_SIZE = 1024  # Message buffer size
```

To modify settings, edit the constants at the top of each file.

## 🎯 Usage Examples

### Basic Echo Test
```
Enter message: Hello, Server!
Server echo: Hello, Server!

Enter message: Testing 123
Server echo: Testing 123

Enter message: exit
Server response: Goodbye!
Disconnected from server
```

### Server Log Example
```
2024-01-15 10:30:45 - INFO - Echo server started on 127.0.0.1:65432
2024-01-15 10:30:45 - INFO - Waiting for client connections...
2024-01-15 10:31:15 - INFO - New client connected: 127.0.0.1:54321
2024-01-15 10:31:25 - INFO - Received from 127.0.0.1:54321: 'Hello, Server!'
2024-01-15 10:31:25 - INFO - Echoed to 127.0.0.1:54321: 'Hello, Server!'
2024-01-15 10:31:30 - INFO - Received from 127.0.0.1:54321: 'exit'
2024-01-15 10:31:30 - INFO - Client 127.0.0.1:54321 requested to exit
2024-01-15 10:31:30 - INFO - Connection with 127.0.0.1:54321 closed
```

## 🛡️ Error Handling

The application handles various error conditions:

- **Connection refused**: When server is not running
- **Unexpected disconnections**: Client crashes or network issues
- **Keyboard interrupts**: Ctrl+C graceful shutdown
- **Socket errors**: Network-related problems
- **Empty messages**: Skipped by client

## 🚪 Exit Methods

### Client Exit Options:
1. Type 'exit' and press Enter (graceful)
2. Press Ctrl+C (interrupt handling)
3. Press Ctrl+D (EOF handling)

### Server Exit:
1. Press Ctrl+C for graceful shutdown

## 🔍 Troubleshooting

### Common Issues

**"Connection refused" error:**
- Ensure the server is running before starting clients
- Check that nothing else is using port 65432

**"Address already in use" error:**
- Wait a few seconds after stopping the server
- The `SO_REUSEADDR` option should prevent this

**Server not responding:**
- Check firewall settings
- Verify localhost connectivity

### Debug Mode

For additional debugging, you can modify the logging level in `server.py`:

```python
logging.basicConfig(level=logging.DEBUG)  # More verbose output
```

## 🔮 Future Enhancements

Potential improvements for learning purposes:

- Add message encryption
- Implement user authentication
- Support for different message protocols
- GUI client interface
- Configuration file support
- Message history logging
- Broadcast messaging capabilities
- IPv6 support

## 📚 Learning Objectives

This project demonstrates:

- **Socket Programming**: IPv4 TCP socket creation and management
- **Threading**: Concurrent client handling with Python threads
- **Network Protocols**: Client-server communication patterns  
- **Error Handling**: Robust network application development
- **Logging**: Professional application monitoring
- **Clean Code**: Well-documented, maintainable Python code

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
