import tcp
import udp
import sys
import multiprocessing
import socket
import gpt

# Define a Server class to handle both TCP and UDP communication
class Server:
    def __init__(self, tcp_server: "tcp.TCPServer", udp_server: "udp.UDPServer") -> "Server":
        # Initialize the server with TCP and UDP instances, and user context storage
        self.tcp_server = tcp_server
        self.udp_server = udp_server
        self.user_context = {}
        # Start the server
        self.start()

    # Process incoming TCP messages from a specific client
    def process_tcp(self, tcp_conn: "tcp.TCPServer.ClientConnection"):
        while True:
            try:
                # Receive a message and the address of the client
                msg, address = tcp_conn.recv_msg()

                # Check if the client wants to disconnect
                if msg.lower() == "q":
                    print(f"Client {address} disconnected\n")
                    tcp_conn.close()
                    break

                # Create a unique key for the user based on IP and port
                address_key = address[0] + ", " + str(address[1])

                # Check if the message is not empty
                if msg:
                    # If the user is new, create a context for them
                    if address_key not in self.user_context:
                        self.user_context[address_key] = {"conversation": []}

                    # Print received message information
                    print(f"\nReceived message from {address}: {msg} over TCP")

                    # If the user wants to clear the context
                    if msg.lower() == "e":
                        self.user_context[address_key]["conversation"] = []
                        print(f"Context cleared for client: {address_key}")
                        continue

                    # Use GPT to generate a response based on the user's message
                    bot = gpt.ChatBot()
                    context = self.user_context[address_key]["conversation"]
                    response = bot.ask(msg, context)

                    # Update the user's conversation history
                    self.user_context[address_key]["conversation"].append(
                        {"role": "user", "content": msg}
                    )

                    # Send the response back to the user
                    if response:
                        try:
                            tcp_conn.send_msg("[TCP] " + response)
                            self.user_context[address_key]["conversation"].append(
                                {"role": "assistant", "content": response}
                            )
                            print(f"Sent message to client: {response}\n")
                        except OverflowError as e:
                            print(e)
                            tcp_conn.send_msg("Encryption failed. Response too long.")
                    else:
                        tcp_conn.send_msg("Something went wrong.")

            except Exception as e:
                print(e)
                continue

    # Process incoming UDP messages
    def process_udp(self):
        while True:
            try:
                # Receive a message and the address of the sender
                msg, address = self.udp_server.recv_msg()
                address_key = address[0] + ", " + str(address[1])

                # Check if the message is not empty
                if msg:
                    # Check if the user wants to disconnect
                    if msg.lower() == "q":
                        print(f"\nClient {address} disconnected")
                        break

                    # Print received message information
                    print(f"Received message from {address}: {msg} over UDP")

                    # If the user wants to clear the context
                    if msg.lower() == "e":
                        self.user_context[address_key]["conversation"] = []
                        print(f"Context cleared for client: {address_key}")
                        continue

                    # Use GPT to generate a response based on the user's message
                    bot = gpt.ChatBot()
                    context = self.user_context.get(address_key, {"conversation": []})[
                        "conversation"
                    ]
                    response = bot.ask(msg, context)

                    # Update the user's conversation history
                    self.user_context[address_key] = {"conversation": context}

                    # Send the response back to the user
                    if response:
                        self.udp_server.send_msg("[UDP] " + response, address)
                        self.user_context[address_key]["conversation"].append(
                            {"role": "assistant", "content": response}
                        )
                        print(f"Sent message to client: {response}")
                    else:
                        self.udp_server.send_msg("Something went wrong.", address)

            except Exception as e:
                print(e)
                break

    # Create a new process to handle a TCP client connection
    def new_tcp_client(self, client: "socket.socket", address: str) -> None:
        conn = tcp.TCPServer.ClientConnection(client, address, self.tcp_server)
        p = multiprocessing.Process(
            target=self.process_tcp, name=str(address), args=[conn]
        )
        p.start()

    # Create a new process to handle UDP messages
    def udp_client(self) -> None:
        p = multiprocessing.Process(target=self.process_udp, name="ProcessUDP")
        p.start()

    # Start the server and continuously listen for incoming connections
    def start(self) -> None:
        print("Server started on IP: ", self.tcp_server.host)
        print("Listening for TCP connections on port", self.tcp_server.port)
        print("Listening for UDP messages on port", self.udp_server.port)
        print()

        while True:
            # Accept a new TCP client connection
            tcp_client, tcp_address = self.tcp_server.accept_connection()
            self.new_tcp_client(tcp_client, tcp_address)

            # Start the process to handle UDP messages
            self.udp_client()

# Entry point of the script
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 4:
        print(
            "Invalid usage, format: python server.py <IP address> <TCP port> <UDP port>"
        )
        exit()

    # Extract command-line arguments
    ip_addr = str(sys.argv[1])
    tcp_port = int(sys.argv[2])
    udp_port = int(sys.argv[3])

    # Create instances of TCP and UDP servers
    tcp_server = tcp.TCPServer(ip_addr, tcp_port)
    udp_server = udp.UDPServer(ip_addr, udp_port)

    # Create and start the server instance
    server = Server(tcp_server, udp_server)
