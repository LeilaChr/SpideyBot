import discord
from discord.ext import commands
import tcp
import udp

handler = None

class Handler:
    def __init__(self) -> None:
        self.udp_client = None
        self.tcp_client = None

    def set_udp_client(self, ip, port):
        self.udp_client = udp.UDPClient(ip, port)

    def set_tcp_client(self, ip, port):
        self.tcp_client = tcp.TCPClient(ip, port)

    def connect(self, ip_dest, udp_port, tcp_port):
        if ip_dest and udp_port and tcp_port:
            self.set_tcp_client(ip_dest, int(tcp_port))
            self.set_udp_client(ip_dest, int(udp_port))
        else:
            print("Invalid IP address or ports")

        if not self.tcp_client or not self.udp_client:
            print("Error connecting to server")

    def disconnect(self):
        if self.udp_client and self.tcp_client:
            self.tcp_client.close()
            self.udp_client.close()

    def send_udp_msg(self, msg):
        if self.udp_client:
            self.udp_client.send_msg(msg)
        else:
            print("No UDP connection established")

    def send_tcp_msg(self, msg):
        if self.tcp_client:
            self.tcp_client.send_msg(msg)
        else:
            print("No TCP connection established")


class msg_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
        ``` ** Commands **
        !connect <ip> <tcp_port> <udp_port> - Connect to the server
        !disconnect - Disconnect from the server
        !send_udp <message> - Send a UDP message
        !send_tcp <message> - Send a TCP message
        !quit - Quit the bot
        ```
        """
    
    
    @commands.command(name="hi", help="Ping the bot")
    async def hi(self, ctx):
        await ctx.send("Hello!")

    @commands.command(name="help", help="Show available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    @commands.command(name="connect", help="Connect to the server")
    async def connect(self, ctx, ip, tcp_port, udp_port):
        print(ip, tcp_port, udp_port)
        global handler
        handler = Handler()
        handler.connect(ip, int(tcp_port), int(udp_port))
        await ctx.send("Connected to the server.")

    @commands.command(name="disconnect", help="Disconnect from the server")
    async def disconnect(self, ctx):
        if handler:
            handler.disconnect()
            await ctx.send("Disconnected from the server.")
        else:
            await ctx.send("No connection to disconnect.")

    @commands.command(name="send_udp", help="Send a UDP message")
    async def send_udp(self, ctx, message):
        if handler:
            handler.send_udp_msg(message)
            await ctx.send("Sent UDP message.")
        else:
            await ctx.send("No UDP connection established.")

    @commands.command(name="send_tcp", help="Send a TCP message")
    async def send_tcp(self, ctx, message):
        if handler:
            handler.send_tcp_msg(message)
            await ctx.send("Sent TCP message.")
        else:
            await ctx.send("No TCP connection established.")

    @commands.command(name="quit", help="Quit the bot")
    async def quit_bot(self, ctx):
        if handler:
            handler.disconnect()
        await ctx.send("Bot has quit.")
        await self.bot.close()