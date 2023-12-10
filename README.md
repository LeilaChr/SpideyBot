# SpideyBot ..
Chatbot that builds on principles of networking such as UDP,TCP packets and encryption. Available in cli,UI, or as a discord bot.
Invokes ChatGpt on input supplied to the bot and relays Gpt's output back to the user.

I. Team members:

	- Mohannad Shehata 1006774787
	- Leila Cheraghi Seifabad  1007465495
 	- Maaz Hashmi 1006804718

II. Rationale:

After learning about networks we wanted to investigate how much we take for granted in our daily use of applications 
from the networking point of view so we started with an existing application and used our newfound networks 
knowledge to connect a user to these services (along with additional features we explore below).

III. Methodology:

We create a server that we can process TCP/UDP requests sent by a client and then extract the messages inside them
and uses them as queries to ChatGpt. After receiving a response it sends the response back to the client. Interactions
between the client and the server are encrypted,and both exchange public keys as soon as the connection is formed.

We allow the client the option to choose between sending either UDP or TCP packages, and it is possible to switch between
both without terminating the program (see below). In addition to the CLI option, we also give the users the possibility of 
using a UI or having it communicate via a discord bot added in the desired server.

The main obstacle we faced was that the server/client behaved differently based on the device they were running on. 
We recommend running it on linux or at least running it in a docker container.

IV. Implementation:

We create a server that can communicate with both ChatGpt and clients. For it to communicate with ChatGpt it uses 
and OpenAI API key which we do not supply here for privacy reasons,but one can easily create their own. To decrease response times 
and make the interaction resemble that of a usual chatbot we first prompt ChatGpt to send shorter messages before sending messages, using
the following:

> "You're a chatbot for a quick one to one chat application with a human. Limit your responses to the following questions to a sentence or 2 max."

We also use multiprocessing to enable the server to run 2 distinct processes to handle TCP and UDP communications respectively.

As for the client, we have multiple versions with similar implemntation principles, or more precisely the mechanism by which they send messages
to the server is similar. The cli one allows users to send messages from the terminal, the UI one allows users to input their queries in a text box
and receive the answer in a format similar to usual desktop applications, while the discord bot interfaces with a particular server. The commands
are entered through a discord chat and read by a client program, which sends it to a server program, receives a response, and then posts the response
back to discord.

For encryption, we generate two RSA key pairs, one for client to server and the other for the reverse direction. The 
party that generated the key pair sends its public key to the other party, establishing a secure communications channel.

V. Instructions for Running the Project 

We strongly advise running the project in a virtual environment(venv), so the first step would be to create our own by running the following:

> sudo apt install python3.10-venv
> python3 -m venv spideybot

After the venv was created, we can setup as follows:

> source spideybot/bin/activate
> pip install -r requirements.txt

Then we should be in the virtual environment with all the needed dependencies to run the project in place. Hereafter we assume
we are running from within the venv, if we close the terminal and open it again the command "source spiderybot/bin/activate" suffices.

- Running the Server

To run the server we run the following command:
> python3 src/server.py <IP> <TCP port> <UDP port>

It awaits client connection and should also display messages when clients connect or disconnect, or upon receiving a message
from a client including the contents of such message.

- Running the CLI client

To run the cli client, we type the following:
> python3 src/client.py

Then when prompted to connect to the server, we input the same IP address, TCP port, and UDP port we used when running the server command above.

Then it should display the following:

![image](https://github.com/LeilaChr/SpideyBot/assets/88001942/0d980be3-127b-4f83-9ed9-fcdea4f84d06)

The user then chooses whether to send UDP,TCP, or disconnect from the server by typing UDP,TCP, or Q respectively. Once the user makes the choice,
they can type their queries to the server and it should reply back.

To switch modes(TCP vs UDP) the user can type E and it will bring them back to the prompt where they choose UDP,TCP, or quit.

- Running the UI client 

To run the UI client, we run the following:
> python3 src/client_ui.py

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


  
