import discord
from discord.ext import commands
import os
import tcp
import udp
import asyncio
from dotenv import load_dotenv

handler = None

class Handler:
    def __init__(self) -> None:
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


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")
help_message = """
        ``` ** Commands **
        !connect <ip> <tcp_port> <udp_port> - Connect to the server
        !disconnect - Disconnect from the server
        !send_udp <message> - Send a UDP message
        !send_tcp <message> - Send a TCP message
        !quit - Quit the bot
        ```
        """
@bot.event
async def on_ready():
    print("Bot is ready")

@bot.command(name="help")
async def help(ctx):
    await ctx.send(help_message)

@bot.command(name="hi")
async def hi(ctx):
    await ctx.send("Hello!")

@bot.command(name="connect", help="Connect to the server")
async def connect(ctx, ip, tcp_port, udp_port):
    global handler
    handler = Handler()
    handler.connect(ip, int(tcp_port), int(udp_port))
    await ctx.send("Connected to the server.")

@bot.command(name="disconnect", help="Disconnect from the server")
async def disconnect( ctx):
    if handler:
        handler.disconnect()
        await ctx.send("Disconnected from the server.")
    else:
        await ctx.send("No connection to disconnect.")

@bot.command(name="send_udp", help="Send a UDP message")
async def send_udp(ctx, *message):
    if handler:
        full_message = ' '.join(message)
        print
        handler.send_udp_msg(full_message)
        await ctx.send("Sent UDP message.")
        text = handler.udp_client.recv_msg()
        if text:
            await ctx.send(text)
        else:
            await ctx.send("No UDP response received.")
    else:
        await ctx.send("No UDP connection established.")

@bot.command(name="send_tcp", help="Send a TCP message")
async def send_tcp( ctx, *message):
    if handler:
        full_message = ' '.join(message)
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

@bot.command(name="quit", help="Quit the bot")
async def quit_bot(ctx):
    if handler:
        handler.disconnect()
    await ctx.send("Bot has quit.")
    await bot.close()



# Run the bot with your Discord token
load_dotenv()
token = str(os.environ.get("DISCORD_TOKEN"))
bot.run(token)
