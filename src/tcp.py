import rsa
import socket

# Define connection types (SERVER and CLIENT)
class ConnectionTypes:
    SERVER = 0
    CLIENT = 1

# Define a TCPHandler class for common TCP functionalities
class TCPHandler:
    def __init__(
        self, type: int, host: str, port: int, private_key=None, public_key=None
    ) -> "TCPHandler":
        # Initialize TCPHandler with necessary parameters
        self.host = host
        self.port = port
        self.type = type

        # Generate RSA key pair if not provided
        if (private_key is None) and (public_key is None):
            self.public_key, self.private_key = self.generate_rsa_key_pair()
        else:
            self.public_key = public_key
            self.private_key = private_key

        # Create a TCP socket instance
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    # Method to generate an RSA key pair
    def generate_rsa_key_pair(self):
        print("\nGenerating RSA key pair...")
        public_key, private_key = rsa.newkeys(4096, poolsize=8)
        return public_key, private_key

    # Method to connect the socket based on the connection type
    def connect_socket(self, connections: int = 5) -> bool:
        match self.type:
            case ConnectionTypes.SERVER:
                # For SERVER, bind and listen for incoming connections
                self.instance.bind((self.host, self.port))
                self.instance.listen(connections)
                return True
            case ConnectionTypes.CLIENT:
                # For CLIENT, connect to the specified host and port
                self.instance.connect((self.host, self.port))
                return True

        return False

    # Method to close the socket
    def close(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False

# TCPServer class, inherits from TCPHandler
class TCPServer(TCPHandler):
    def __init__(self, host: str, port: int):
        # Initialize TCPServer, inheriting from TCPHandler
        self.handler = super(TCPServer, self).__init__(
            ConnectionTypes.SERVER, host, port
        )
        # Set public and private keys from the handler
        self.public_key = self.handler.public_key
        self.private_key = self.handler.private_key
        # Connect the socket
        self.handler.connect_socket()

    # Method to accept a new TCP client connection
    def accept_connection(self) -> tuple[socket.socket, str]:
        client, address = self.handler.instance.accept()
        return client, address

    # Inner class for handling a specific TCP client connection
    class ClientConnection:
        def __init__(self, client, address, server):
            # Initialize a new TCP connection
            self.client = client
            self.address = address
            self.public_key = server.public_key
            self.private_key = server.private_key
            print(f"New TCP connection from {self.address}")
            print("Exchanging public keys...")
            self.exchange_keys()

        # Method to exchange public keys with the client
        def exchange_keys(self) -> bool:
            try:
                # Send the server's public key to the client
                self.client.send(self.public_key.save_pkcs1())
                # Receive the client's public key
                client_public_key = self.client.recv(4096)
                # Load the client's public key
                self.client_public_key = rsa.PublicKey.load_pkcs1(client_public_key)
                print("\nSuccessfully exchanged public keys!")
                return True
            except Exception as e:
                print(e)
                return False

        # Method to send an encrypted message to the client
        def send_msg(self, message: str) -> tuple[int, str]:
            encrypted_message = rsa.encrypt(
                message.encode("utf-8"), self.client_public_key
            )
            return self.client.send(encrypted_message), encrypted_message

        # Method to receive and decrypt a message from the client
        def recv_msg(self) -> tuple[str, str]:
            encoded_response = self.client.recv(4096)
            decrypted_response = rsa.decrypt(encoded_response, self.private_key).decode(
                "utf-8"
            )
            return decrypted_response, self.address

        # Method to close the client connection
        def close(self) -> bool:
            try:
                self.client.close()
                return True
            except Exception as e:
                print(e)
                return False

# TCPClient class, inherits from TCPHandler
class TCPClient(TCPHandler):
    def __init__(self, host: str, port: int):
        # Initialize TCPClient, inheriting from TCPHandler
        self.handler = super(TCPClient, self).__init__(
            ConnectionTypes.CLIENT, host, port
        )
        # Set public and private keys from the handler
        self.public_key = self.handler.public_key
        self.private_key = self.handler.private_key
        # Connect the socket and exchange keys
        self.handler.connect_socket()
        self.exchange_keys()

    # Method to exchange public keys with the server
    def exchange_keys(self) -> bool:
        try:
            # Send the client's public key to the server
            self.handler.instance.send(self.public_key.save_pkcs1())
            # Receive the server's public key
            server_public_key = self.handler.instance.recv(4096)
            # Load the server's public key
            self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key)
            print("\nSuccessfully exchanged public keys!\n")
            return True
        except Exception as e:
            print(e)
            return False

    # Method to send an encrypted message to the server
    def send_msg(self, message: str) -> int:
        encrypted_message = rsa.encrypt(message.encode("utf-8"), self.server_public_key)
        return self.handler.instance.send(encrypted_message)

    # Method to receive and decrypt a message from the server
    def recv_msg(self) -> str:
        encoded_response = self.handler.instance.recv(4096)
        decrypted_response = rsa.decrypt(encoded_response, self.private_key).decode(
            "utf-8"
        )
        return decrypted_response
