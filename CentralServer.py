# Central Server

import os
import select
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local server
serverAddress = ('localhost', 10000)
print("Starting on %s port %s" % serverAddress)
sock.bind(serverAddress)
sock.listen(1)

# Create an array to hold a table of user information.
allUsers = []

# Create an array to remember previous users.
prevUsers = []

# Create an array to hold a table of user file descriptions/
fileDesc = []

# Starts the connection process with the client.
while (True):
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()

    # Tells the user the connection is successful.
    try:

        # Gets the user that connected and add to user table
        user = connection.recv(1024).decode()
        user = user.split(" ")
        allUsers.append(user)
        print("Connection with ", clientAddress)
        print("User: ", user[0])

        # Check if first time using this server.



        # Listens for the selected input from the client.
        while (True):
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("Received: %s\n" % data)
            if (data):

                # Send a list of current users.
                if (command[0] == "USER_LIST"):
                    connection.sendall(allUsers)

                # Do a keyword search.
                if (command[0] == "KEYWORD_SEARCH"):
                    #something

                # Get a file description.
                if (command[0] == "FILE_DESC"):
                    thisDesc = [user[0], command[1]]
                    fileDesc.append(thisDesc)

                # Closes the connection with the server.
                elif (command[0] == "QUIT"):

                    # Remove user from user list.
                    allUsers.remove(user)

                    # Remove file description by this user.
                    needRemove = [x for x in fileDesc if user[0] not in fileDesc]

                    for x in needRemove:
                        fileDesc.remove(needRemove[x])

                    # Close connection
                    connection.close()
                    break

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Closing connection")
        connection.close()
