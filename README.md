# SpideyBot

ChatBot that builds on principles of networking such as UDP, TCP packets and encryption. Available in CLI, UI, or as a Discord bot.
Invokes OpenAI’s GPT-3.5-turbo LLM on input supplied to the bot and relays GPT's output back to the user.

# Report

See `report.pdf` for detailed analysis, descriptions and implementation details.

# Team Members

    - Mohannad Shehata 1006774787
    - Leila Cheraghi Seifabad 1007465495
    - Maaz Hashmi 1006804718

# Usage

We strongly advise running the project in a virtual environment (venv) and using Linux machine or a Docker container (see below). Firstly, add the `.env` provided with the submission to the `src/` directory. The next step would be to create our own by running the following:

`sudo apt install python3.10-venv`

`python3 -m venv spideybot`

After the venv was created, we can setup as follows:

`source spideybot/bin/activate`

`pip install -r requirements.txt`

Then we should be in the virtual environment with all the needed dependencies to run the project in place. Hereafter we assume
we are running from within the venv, if we close the terminal and open it again the command "source spideybot/bin/activate" suffices.

Moreover, one would have to create a .env file and add both their own OpenAI API key for the server to communicate with GPT
and their own discord token so the bot version of the client can access the server and read the chat to interact with the user>

## Running the Server

To run the server we run the following command:

`python3 src/server.py <IP> <TCP port> <UDP port>`

It awaits client connection and should also display messages when clients connect or disconnect, or upon receiving a message
from a client including the contents of such message.

## Running the CLI client

To run the cli client, we type the following:

`python3 src/client.py`

Then when prompted to connect to the server, we input the same IP address, TCP port, and UDP port we used when running the server command above.

Then it should display the following:

![image](https://github.com/LeilaChr/SpideyBot/assets/88001942/0d980be3-127b-4f83-9ed9-fcdea4f84d06)

The user then chooses whether to send UDP,TCP, or disconnect from the server by typing UDP,TCP, or Q respectively. Once the user makes the choice,
they can type their queries to the server and it should reply back.

To switch modes(TCP vs UDP) the user can type E and it will bring them back to the prompt where they choose UDP,TCP, or quit.

## Running the UI client

To run the UI client, we run the following:

`python3 src/client_ui.py`

The following image should appear after a successful execution

![image](https://github.com/LeilaChr/SpideyBot/assets/88001942/d3f9292d-692c-4146-9b88-df2de5fb2c61)

We then fill out the IP address and TCP/UDP port info in the same fashion as the CLI client in the respective text boxes.
After that we press connect and if the connection was successful we should get a popup message as follows

![image](https://github.com/LeilaChr/SpideyBot/assets/88001942/f0af2743-7346-4f0b-87c2-654704a237f0)

Then we can type the message in the message textbox and click "Send TCP" or "Send UDP" to send using the respective format
It should display a popup message saying the message was sent successfully and, upon clicking ok, display the actual
response in a popup message as follows

![image](https://github.com/LeilaChr/SpideyBot/assets/88001942/4253a026-ac95-492a-a085-715c8af4bc85)

Finally to close the connection one can click quit.

## Running the Discord client

In order to use the Discord client, firstly add our Discord bot to a Discord server of your choosing, using the following link: https://discord.com/api/oauth2/authorize?client_id=1179101192912113794&permissions=274877983808&scope=bot. Note that you must have admin permissions to this server.

To run the bot, we type the following:

`python3 src/client_discord.py`

Then we go to the discord channel where this bot has a token (remember you have to add the token to the .env file), we can type any of the following commands in the chat:

> !hi

The reply will be Hello!

> !help

Prints the commands the bot has along with a summary of their use

> !connect \<IP> \<TCP port> \<UDP port>

Connects to the server with these details

> !disconnect

Disconnects from the server

> !send_tcp \<message>

Sends a \<message> as a tcp packet to the server and prints out the server's response

> !send_udp \<message>

Sends a \<message> as a udp packet to the server and prints out the server's response

> !quit

Shuts the discord bot down

Note that the first two commands do not require a connection to the server

## Docker

An alternative to running the cli or discord client using docker containers is as follows:

- run `docker build -t spideybot .`
- then `docker run -it spideybot`
- open up a new terminal and run `docker ps` and copy the container id for spideybot
- in the new terminal run `docker exec -it <CONTAINER-ID> bash`
- now in one terminal run server.py like we do `python3 src/server.py localhost 3000 3001`
- and in the other run the client `python3 src/client_cli.py`
