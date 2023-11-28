import tkinter as tk
from tkinter import messagebox
import tcp
import udp

class Handler:
    def __init__(self):
        self.udp_client = None
        self.tcp_client = None

    def set_udp_client(self, ip, port):
        self.udp_client = udp.UDPClient(ip, port)

    def set_tcp_client(self, ip, port):
        self.tcp_client = tcp.TCPClient(ip, port)

    def connect(self, ip_dest, tcp_port, udp_port):
        if ip_dest and udp_port and tcp_port:
            self.set_tcp_client(ip_dest, int(tcp_port))
            self.set_udp_client(ip_dest, int(udp_port))
            messagebox.showinfo("Success", "Successfully connected to server")
        else:
            messagebox.showerror("Error", "Invalid IP address or ports")

        if not self.tcp_client or not self.udp_client:
            messagebox.showerror("Error", "Error connecting to server")

    def disconnect(self):
        if self.udp_client and self.tcp_client:
            self.tcp_client.close()
            self.udp_client.close()
        root.destroy()

    def send_udp_msg(self):
        if self.udp_client:
            msg = entry_msg.get()
            self.udp_client.send_msg(msg)
            messagebox.showinfo("Success", "Successfully sent UDP message")
        else:
            messagebox.showerror("Error", "No UDP connection established")

    def send_tcp_msg(self):
        if self.tcp_client:
            msg = entry_msg.get()
            self.tcp_client.send_msg(msg)
            messagebox.showinfo("Success", "Successfully sent TCP message")
        else:
            messagebox.showerror("Error", "No TCP connection established")

def handle_protocol(protocol):
    if protocol.lower() == "udp":
        handler.send_udp_msg()
        text = handler.udp_client.recv_msg()
        if text:
            label.config(text=text)
            messagebox.showinfo("Success", text)
    elif protocol.lower() == "tcp":
        handler.send_tcp_msg()
        text = handler.tcp_client.recv_msg()
        if text:
            label.config(text=text)
            messagebox.showinfo("Success", text)
    elif protocol.lower() == "q":
        handler.disconnect()
    else:
        messagebox.showerror("Error", "Invalid protocol. Please try again.")

handler = Handler()

root = tk.Tk()
root.geometry("600x600")

frame = tk.Frame(root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = tk.Label(frame, text="IP Address")
label.pack(pady=10)

entry1 = tk.Entry(frame, text="IP Address")
entry1.pack(pady=6, padx=5)

label = tk.Label(frame, text="TCP Port")
label.pack(pady=10)

entry2 = tk.Entry(frame, text="TCP Port")
entry2.pack(pady=6, padx=5)

label = tk.Label(frame, text="UDP Port")
label.pack(pady=10)

entry3 = tk.Entry(frame, text="UDP Port")
entry3.pack(pady=6, padx=5)

button_connect = tk.Button(frame, text="Connect to server", command=lambda: handler.connect(entry1.get(), entry2.get(), entry3.get()))
button_connect.pack(pady=12, padx=10)

label = tk.Label(frame, text="Message")
label.pack(pady=10)

entry_msg = tk.Entry(frame, text="Enter message")
entry_msg.pack(pady=10, padx=10)

button_udp = tk.Button(frame, text="Send UDP", command=lambda: handle_protocol("udp"))
button_udp.pack(pady=12, padx=10)

button_tcp = tk.Button(frame, text="Send TCP", command=lambda: handle_protocol("tcp"))
button_tcp.pack(pady=12, padx=10)

button_quit = tk.Button(frame, text="Quit (Q)", command=lambda: handle_protocol("q"))
button_quit.pack(pady=12, padx=10)

root.mainloop()
