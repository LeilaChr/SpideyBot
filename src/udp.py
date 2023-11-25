import socket


class ConnectionTypes:
    SERVER = 0
    CLIENT = 1


class UDPServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.instance.bind((host, port))

    def send_msg(self, message: str, address: tuple[str, int]) -> int:
        encrypted_message = message
        return self.instance.sendto(str.encode(encrypted_message, "UTF-8"), address)

    def recv_msg(self) -> tuple[str, str]:
        encoded_message, address = self.instance.recvfrom(4096)
        decoded_message = encoded_message.decode("utf-8")
        return decoded_message, address

    def close(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False


class UDPClient:
    def __init__(self, host: str, port: int) -> None:
        self.instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    def send_msg(self, message: str) -> int:
        encrypted_messsage = message
        return self.instance.sendto(
            str.encode(encrypted_messsage, "UTF-8"), (self.host, self.port)
        )

    def recv_msg(self) -> str:
        encoded_message, _ = self.instance.recvfrom(4096)
        decoded_message = encoded_message.decode("utf-8")
        return decoded_message

    def close_connection(self) -> bool:
        try:
            self.instance.close()
            return True
        except Exception as e:
            print(e)
            return False
