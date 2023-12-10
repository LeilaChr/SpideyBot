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
            return 1
        else:
            print("Invalid IP address or ports")
            return 0
        if not self.tcp_client or not self.udp_client:
            print("Error connecting to server")
            return 0
            		
    def disconnect(self):
        if self.udp_client is not None:
            self.udp_client.close()
        if self.tcp_client is not None:
            self.tcp_client.close()

    def send_udp_msg(self, msg):
        if self.udp_client is not None:
            self.udp_client.send_msg(msg)
        else:
            print("No UDP connection established")

    def send_tcp_msg(self, msg):
        if self.tcp_client is not None:
            self.tcp_client.send_msg(msg)
        else:
            print("No TCP connection established")


handler = Handler()
while(not handler.connect(ip_addr, udp_port, tcp_port)):
	ip_addr = input("IP Address: ")
	tcp_port = input("TCP Port: ")
	udp_port = input("UDP Port: ")

while True:
    protocol = input(
        "\nSelect Protocol [TCP/UDP] (Q to Quit) (E to exit from conversation): "
    )
    if protocol.lower() == "udp":
        while True:
            msg = input(">>> ")
            if msg.lower() == "e":
                handler.send_udp_msg(msg)
                break
            elif msg.lower() == "q":
                handler.send_tcp_msg("q")
                handler.send_udp_msg("q")
                handler.disconnect()
                exit(0)
            handler.send_udp_msg(msg)
            text = handler.udp_client.recv_msg()
            if text:
                print(text + "\n")
            else:
                break
    elif protocol.lower() == "tcp":
        while True:
            msg = input(">>> ")
            if msg.lower() == "e":
                handler.send_tcp_msg(msg)
                break
            elif msg.lower() == "q":
                handler.send_tcp_msg("q")
                handler.send_udp_msg("q")
                handler.disconnect()
                exit(0)
            handler.send_tcp_msg(msg)
            text = handler.tcp_client.recv_msg()
            if text:
                print(text + "\n")
            else:
                break
    elif protocol.lower() == "q":
        handler.send_tcp_msg("q")
        handler.send_udp_msg("q")
        handler.disconnect()
        break
    else:
        print("Invalid protocol. Please try again.")
