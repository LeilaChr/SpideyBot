import socket


class ConnectionTypes:
    SERVER = 0
    CLIENT = 1


class TCPHandler:
    def __init__(self, type: int, host: str, port: int) -> "TCPHandler":
        self.host = host
        self.port = port
        self.type = type
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

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
        self.handler.connect_socket()

    def accept_connection(self) -> tuple[socket.socket, str]:
        client, address = self.handler.instance.accept()
        return client, address

    class ClientConnection:
        def __init__(self, client, address):
            self.client = client
            self.address = address

        def send_msg(self, message: str) -> int:
            # TODO: encryption
            encrypted_messsage = message
            return self.client.send(str.encode(encrypted_messsage, "UTF-8"))

        def recv_msg(self) -> tuple[str, str]:
            encoded_response = self.client.recv(4096)
            decoded_response = encoded_response.decode("utf-8")
            # TODO: decryption
            decrypted_response = decoded_response

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
        self.handler.connect_socket()

    def send_msg(self, message: str) -> int:
        # TODO: encryption
        encrypted_messsage = message
        return self.handler.instance.send(str.encode(encrypted_messsage, "UTF-8"))

    def recv_msg(self) -> str:
        encoded_response = self.handler.instance.recv(4096)
        decoded_response = encoded_response.decode("utf-8")
        # TODO: decryption
        decrypted_response = decoded_response
        return decrypted_response
