import rsa
import socket


class ConnectionTypes:
    SERVER = 0
    CLIENT = 1


class TCPHandler:
    def __init__(
        self, type: int, host: str, port: int, private_key=None, public_key=None
    ) -> "TCPHandler":
        self.host = host
        self.port = port
        self.type = type
        if (private_key is None) and (public_key is None):
            self.public_key, self.private_key = self.generate_rsa_key_pair()
        else:
            self.public_key = public_key
            self.private_key = private_key
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def generate_rsa_key_pair(self):
        print("\nGenerating RSA key pair...")
        public_key, private_key = rsa.newkeys(4096, poolsize=8)
        return public_key, private_key

    def connect_socket(self, connections: int = 5) -> bool:
        match self.type:
            case ConnectionTypes.SERVER:
                self.instance.bind((self.host, self.port))
                self.instance.listen(connections)
                return True
            case ConnectionTypes.CLIENT:
                self.instance.connect((self.host, self.port))
                return True

        return False

    def close(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False


class TCPServer(TCPHandler):
    def __init__(self, host: str, port: int):
        self.handler = super(TCPServer, self).__init__(
            ConnectionTypes.SERVER, host, port
        )
        self.public_key = self.handler.public_key
        self.private_key = self.handler.private_key
        self.handler.connect_socket()

    def accept_connection(self) -> tuple[socket.socket, str]:
        client, address = self.handler.instance.accept()
        return client, address

    class ClientConnection:
        def __init__(self, client, address, server):
            self.client = client
            self.address = address
            self.public_key = server.public_key
            self.private_key = server.private_key
            print(f"New TCP connection from {self.address}")
            print("Exchanging public keys...")
            self.exchange_keys()

        def exchange_keys(self) -> bool:
            try:
                self.client.send(self.public_key.save_pkcs1())
                client_public_key = self.client.recv(4096)
                self.client_public_key = rsa.PublicKey.load_pkcs1(client_public_key)
                print("\nSuccessfully exchanged public keys!")
                return True
            except Exception as e:
                print(e)
                return False

        def send_msg(self, message: str) -> tuple[int, str]:
            # print(f"\nServer sending message: {message}\n")
            # print("\nEncrypting using client's public key\n")
            encrypted_message = rsa.encrypt(
                message.encode("utf-8"), self.client_public_key
            )
            # print("Server encrypted message: ", encrypted_message)
            return self.client.send(encrypted_message), encrypted_message

        def recv_msg(self) -> tuple[str, str]:
            encoded_response = self.client.recv(4096)
            # print(f"\nServer receiving message: {encoded_response}\n")
            # print("Decrypting using server's private key...")
            decrypted_response = rsa.decrypt(encoded_response, self.private_key).decode(
                "utf-8"
            )
            # print("Server decrypted message: ", decrypted_response)
            return decrypted_response, self.address

        def close(self) -> bool:
            try:
                self.client.close()
                return True
            except Exception as e:
                print(e)
                return False


class TCPClient(TCPHandler):
    def __init__(self, host: str, port: int):
        self.handler = super(TCPClient, self).__init__(
            ConnectionTypes.CLIENT, host, port
        )
        self.public_key = self.handler.public_key
        self.private_key = self.handler.private_key
        self.handler.connect_socket()
        self.exchange_keys()

    def exchange_keys(self) -> bool:
        try:
            self.handler.instance.send(self.public_key.save_pkcs1())
            server_public_key = self.handler.instance.recv(4096)
            self.server_public_key = rsa.PublicKey.load_pkcs1(server_public_key)
            print("\nSuccessfully exchanged public keys!\n")
            return True
        except Exception as e:
            print(e)
            return False

    def send_msg(self, message: str) -> int:
        # print(f"\nClient sending message: {message}\n")
        # print("\nEncrypting using server public key...\n")
        encrypted_message = rsa.encrypt(message.encode("utf-8"), self.server_public_key)
        # print("Client encrypted message: ", encrypted_message)
        return self.handler.instance.send(encrypted_message)

    def recv_msg(self) -> str:
        encoded_response = self.handler.instance.recv(4096)
        # print(f"\nClient receiving message: {encoded_response}\n")
        # print("Decrypting using client private key...")
        decrypted_response = rsa.decrypt(encoded_response, self.private_key).decode(
            "utf-8"
        )
        # print("Client decrypted message: ", decrypted_response)
        return decrypted_response
