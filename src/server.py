import tcp
import udp
import sys
import multiprocessing
import socket


class Server:
    def __init__(
        self, tcp_server: "tcp.TCPServer", udp_server: "udp.UDPServer"
    ) -> "Server":
        self.tcp_server = tcp_server
        self.udp_server = udp_server
        self.start()

    def process_tcp(self, tcp_conn: "tcp.TCPServer.ClientConnection"):
        while True:
            try:
                msg, address = tcp_conn.recv_msg()
                if msg:
                    print(f"Received message from {address}: {msg}")
                    response = "TCP"
                    if response:
                        tcp_conn.send_msg(response)
                        print(f"Sent message to client: {response}")
                    else:
                        tcp_conn.send_msg("Something went wrong.")

            except Exception as e:
                print(e)
                continue

    def process_udp(self):
        while True:
            try:
                msg, address = self.udp_server.recv_msg()
                if msg:
                    print(f"Received message from {address}: {msg}")
                    response = "UDP"
                    if response:
                        self.udp_server.send_msg(response, address)
                    else:
                        self.udp_server.send_msg("Something went wrong.", address)

            except Exception as e:
                print(e)
                break

    def new_tcp_client(self, client: "socket.socket", address: str) -> None:
        conn = tcp.TCPServer.ClientConnection(client, address)
        p = multiprocessing.Process(
            target=self.process_tcp, name=str(address), args=[conn]
        )
        p.start()

    def udp_client(self) -> None:
        p = multiprocessing.Process(target=self.process_udp, name="ProcessUDP")
        p.start()

    def start(self) -> None:
        print("Server started on IP: ", self.tcp_server.host)
        print("Listening for TCP connections on port", self.tcp_server.port)
        print("Listening for UDP messages on port", self.udp_server.port)
        print()

        while True:
            tcp_client, tcp_address = self.tcp_server.accept_connection()
            self.new_tcp_client(tcp_client, tcp_address)
            self.udp_client()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Invalid usage, format: python server.py <IP address> <TCP port> <UDP port>"
        )
        exit()

    ip_addr = str(sys.argv[1])
    tcp_port = int(sys.argv[2])
    udp_port = int(sys.argv[3])

    tcp_server = tcp.TCPServer(ip_addr, tcp_port)
    udp_server = udp.UDPServer(ip_addr, udp_port)
    server = Server(tcp_server, udp_server)
