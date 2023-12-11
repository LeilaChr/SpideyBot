import tcp
import udp

# Get user input for server IP address, TCP port, and UDP port
ip_addr = input("IP Address: ")
tcp_port = input("TCP Port: ")
udp_port = input("UDP Port: ")

# Handler class for managing TCP and UDP connections
class Handler:
    def __init__(self) -> None:
        self.udp_client = None
        self.tcp_client = None

    # Method to set up UDP client
    def set_udp_client(self, ip, port):
        self.udp_client = udp.UDPClient(ip, port)

    # Method to set up TCP client
    def set_tcp_client(self, ip, port):
        self.tcp_client = tcp.TCPClient(ip, port)

    # Method to connect to the server with the given IP, UDP port, and TCP port
    def connect(self, ip_dest, udp_port, tcp_port):
        # Check if the provided IP, UDP port, and TCP port are valid
        if ip_dest != "" and udp_port != "" and tcp_port != "":
            # Set up TCP and UDP clients
            self.set_tcp_client(ip_dest, int(tcp_port))
            self.set_udp_client(ip_dest, int(udp_port))
            return 1  # Connection successful
        else:
            print("Invalid IP address or ports")
            return 0  # Connection failed        if not self.tcp_client or not self.udp_client:
        if not self.tcp_client or not self.udp_client:
            print("Error connecting to server")
            return 0

    # Method to disconnect from both TCP and UDP connections
    def disconnect(self):
        if self.udp_client is not None:
            self.udp_client.close()
        if self.tcp_client is not None:
            self.tcp_client.close()

    # Method to send a UDP message
    def send_udp_msg(self, msg):
        if self.udp_client is not None:
            self.udp_client.send_msg(msg)
        else:
            print("No UDP connection established")

    # Method to send a TCP message
    def send_tcp_msg(self, msg):
        if self.tcp_client is not None:
            self.tcp_client.send_msg(msg)
        else:
            print("No TCP connection established")

# Create a Handler instance
handler = Handler()

# Try to connect to the server until successful
while(not handler.connect(ip_addr, udp_port, tcp_port)):
	ip_addr = input("IP Address: ")
	tcp_port = input("TCP Port: ")
	udp_port = input("UDP Port: ")

# Main loop for user interaction
while True:
    # Prompt the user to select a protocol (TCP or UDP)
    protocol = input(
        "\nSelect Protocol [TCP/UDP] (Q to Quit) (E to exit from conversation): "
    )

    # Handle user input for UDP protocol
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

    # Handle user input for TCP protocol
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

    # Quit the application if user input is 'Q'
    elif protocol.lower() == "q":
        handler.send_tcp_msg("q")
        handler.send_udp_msg("q")
        handler.disconnect()
        break

    # Handle invalid protocol input
    else:
        print("Invalid protocol. Please try again.")
