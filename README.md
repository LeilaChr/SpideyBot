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
knowledge to connect a user to these services (along with additional features we outline below).

III. Methodology:

We create a server that we can process TCP/UDP requests sent by a client and then extract the messages inside them
and uses them as queries to ChatGpt. After receiving a response it sends the response back to the client. Interactions
between the client and the server are encrypted,and both exchange public keys as soon as the connection is formed.

We allow the client the option to choose between sending either UDP or TCP packages, and it is possible to switch between
both without terminating the program (see below). In addition to the CLI option, we also give the users the possibility of 
using an AI or having it communicate via a discord bot added in the desired server.

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
