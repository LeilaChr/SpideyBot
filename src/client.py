import tcp
import udp

ip_addr = input("IP Address: ")
tcp_port = input("TCP Port: ")
udp_port = input("UDP Port: ")


class Handler:
    def __init__(self) -> None:
        self.udp_client = None
        self.tcp_client = None

    def set_udp_client(self, ip, port):
        self.udp_client = udp.UDPClient(ip, port)

    def set_tcp_client(self, ip, port):
        self.tcp_client = tcp.TCPClient(ip, port)

    def connect(self, ip_dest, udp_port, tcp_port):
        if ip_dest != "" and udp_port != "" and tcp_port != "":
            self.set_tcp_client(ip_dest, int(tcp_port))
            self.set_udp_client(ip_dest, int(udp_port))
        else:
            print("Invalid IP address or ports")

        if not self.tcp_client or not self.udp_client:
            print("Error connecting to server")

    def disconnect(self):
        if self.udp_client != None and self.tcp_client != None:
            self.tcp_client.close()
            self.udp_client.close()

    def send_udp_msg(self, msg):
        if self.udp_client != None:
            self.udp_client.send_msg(msg)
        else:
            print("No UDP connection established")

    def send_tcp_msg(self, msg):
        if self.tcp_client != None:
            self.tcp_client.send_msg(msg)
        else:
            print("No TCP connection established")


handler = Handler()
handler.connect(ip_addr, udp_port, tcp_port)

while True:
    protocol = input("Select Protocol [TCP/UDP] (Q to Quit): ")
    if protocol.lower() == "udp":
        msg = input(">>> ")
        handler.send_udp_msg(msg)
        text = handler.udp_client.recv_msg()
        if text:
            print(text)
    elif protocol.lower() == "tcp":
        msg = input(">>> ")
        handler.send_tcp_msg(msg)
        text = handler.tcp_client.recv_msg()
        if text:
            print(text)
    elif protocol.lower() == "q":
        handler.disconnect()
        break
    else:
        print("Invalid protocol. Please try again.")
