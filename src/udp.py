import socket

# Define connection types (SERVER and CLIENT)
class ConnectionTypes:
    SERVER = 0
    CLIENT = 1

# UDPServer class for handling UDP server functionality
class UDPServer:
    def __init__(self, host: str, port: int):
        # Initialize UDPServer with host and port
        self.host = host
        self.port = port
        # Create a UDP socket instance and bind to the specified host and port
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.instance.bind((host, port))

    # Method to send an encrypted message to a specified address
    def send_msg(self, message: str, address: tuple[str, int]) -> int:
        encrypted_message = message
        return self.instance.sendto(str.encode(encrypted_message, "UTF-8"), address)

    # Method to receive an encrypted message and the sender's address
    def recv_msg(self) -> tuple[str, str]:
        encoded_message, address = self.instance.recvfrom(4096)
        decoded_message = encoded_message.decode("utf-8")
        return decoded_message, address

    # Method to close the UDP socket
    def close(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False

# UDPClient class for handling UDP client functionality
class UDPClient:
    def __init__(self, host: str, port: int) -> None:
        # Initialize UDPClient with host and port
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    # Method to send an encrypted message to the server
    def send_msg(self, message: str) -> int:
        encrypted_message = message
        return self.instance.sendto(
            str.encode(encrypted_message, "UTF-8"), (self.host, self.port)
        )

    # Method to receive an encrypted message from the server
    def recv_msg(self) -> str:
        encoded_message, _ = self.instance.recvfrom(4096)
        decoded_message = encoded_message.decode("utf-8")
        return decoded_message

    # Method to close the UDP socket
    def close(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False
