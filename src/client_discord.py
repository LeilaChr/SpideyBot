import discord
from discord.ext import commands
import os
import tcp
import udp
import asyncio
from dotenv import load_dotenv

# Initialize handler as None
handler = None

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
    def connect(self, ip_dest, tcp_port, udp_port):
        # Check if the provided IP, UDP port, and TCP port are valid
        if ip_dest and udp_port and tcp_port:
            # Set up TCP and UDP clients
            self.set_tcp_client(ip_dest, int(tcp_port))
            self.set_udp_client(ip_dest, int(udp_port))
        else:
            print("Invalid IP address or ports")

        # Check if both TCP and UDP clients are successfully set up
        if not self.tcp_client or not self.udp_client:
            print("Error connecting to server")

    # Method to disconnect from both TCP and UDP connections
    def disconnect(self):
        if self.udp_client and self.tcp_client:
            self.tcp_client.close()
            self.udp_client.close()

    # Method to send a UDP message
    def send_udp_msg(self, msg):
        if self.udp_client:
            self.udp_client.send_msg(msg)
        else:
            print("No UDP connection established")

    # Method to send a TCP message
    def send_tcp_msg(self, msg):
        if self.tcp_client:
            self.tcp_client.send_msg(msg)
        else:
            print("No TCP connection established")


# Set up Discord bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")  # Remove default help command

# Help message for bot commands
help_message = """
        ``` ** Commands **
        !connect <ip> <tcp_port> <udp_port> - Connect to the server
        !disconnect - Disconnect from the server
        !send_udp <message> - Send a UDP message
        !send_tcp <message> - Send a TCP message
        !quit - Quit the bot
        ```
        """


# Event handler for bot on_ready
@bot.event
async def on_ready():
    print("Bot is ready")


# Command to display help message
@bot.command(name="help")
async def help(ctx):
    await ctx.send(help_message)


# Command to greet the bot
@bot.command(name="hi")
async def hi(ctx):
    await ctx.send("Hello!")


# Command to connect to the server
@bot.command(name="connect", help="Connect to the server")
async def connect(ctx, ip, tcp_port, udp_port):
    await ctx.send("Connecting to the server...")
    global handler
    handler = Handler()
    handler.connect(ip, int(tcp_port), int(udp_port))
    await ctx.send("Successfully connected to the server and exchanged public keys.")


# Command to disconnect from the server
@bot.command(name="disconnect", help="Disconnect from the server")
async def disconnect(ctx):
    if handler:
        handler.send_tcp_msg("q")
        handler.send_udp_msg("q")
        handler.disconnect()
        await ctx.send("Disconnected from the server.")
    else:
        await ctx.send("No connection to disconnect.")


# Command to send a UDP message
@bot.command(name="send_udp", help="Send a UDP message")
async def send_udp(ctx, *message):
    if handler:
        full_message = " ".join(message)
        handler.send_udp_msg(full_message)
        await ctx.send("Sent UDP message.")
        text = handler.udp_client.recv_msg()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("No UDP response received.")
    else:
        await ctx.send("No UDP connection established.")


# Command to send a TCP message
@bot.command(name="send_tcp", help="Send a TCP message")
async def send_tcp(ctx, *message):
    if handler:
        full_message = " ".join(message)
        handler.send_tcp_msg(full_message)
        await ctx.send("Sent TCP message.")
        await asyncio.sleep(2)

        text = handler.tcp_client.recv_msg()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("No TCP response received.")
    else:
        await ctx.send("No TCP connection established.")


# Command to quit the bot
@bot.command(name="quit", help="Quit the bot")
async def quit_bot(ctx):
    if handler:
        handler.send_tcp_msg("q")
        handler.send_udp_msg("q")
        handler.disconnect()
    await ctx.send("Bot has quit.")
    await bot.close()


# Load Discord token from .env file
load_dotenv()
token = str(os.environ.get("DISCORD_TOKEN"))
bot.run(token)
