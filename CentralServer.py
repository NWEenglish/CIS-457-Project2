# Central Server
import socket
import _thread
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Local server
serverAddress = ('localhost', 10000)
print("Starting on %s port %s" % serverAddress)
sock.bind(serverAddress)
sock.listen(1)

# Create an array to hold a table of user information.
allUsers = []

# Create an array to hold a table of user file descriptions.
fileDesc = []

# Create an array to hold the full description of all files.
fullDesc = []

# Array that holds what file is owned by who
author = []

# List that holds the identity of all users who have connected.
identityList = []

# All connections
allConns = []


def clientThread(connection):
    # Tells the user the connection is successful.
    try:

        # Gets the user that connected and add to user table
        user = connection.recv(1024).decode()
        user = user.split(" ")
        allConns.append(connection)

        identityList.append(user[0])
        identityList.append(user[1])
        identityList.append(user[2])
        identityList.append(user[3])
        identityList.append(str(clientAddress))

        print("Connection with ", clientAddress)
        print("User: ", user[0])

        # Listens for the selected input from the client.
        while True:
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("Received: %s\n" % data)
            if data:

                # Do a keyword search.
                if command[0] == "KEYWORD_SEARCH":
                    term = command[1]
                    foundWho = ""

                    whoHasTerm = ";".join(s for s in fullDesc if term.lower() in s.lower())
                    whoHasTerm = whoHasTerm.split(";")

                    # Remove empty items.
                    while '' in whoHasTerm:
                        whoHasTerm.remove('')

                    # Concat all items with matching descriptions for the client.
                    for x in whoHasTerm:
                        foundWho += fileDesc[fullDesc.index(x)] + ";"

                    connection.sendall(foundWho.encode())

                # Get a file description.
                elif command[0] == "FILE_DESC":
                    desc = connection.recv(1024).decode()
                    desc = desc.split(";")
                    j = 0

                    # Find the IP with Port from the current connected client.
                    thisIPAndPort = str(connection)
                    thisIPAndPort = thisIPAndPort.split("=")
                    thisIPAndPort = thisIPAndPort[len(thisIPAndPort) - 1]
                    thisIPAndPort = thisIPAndPort[0:(len(thisIPAndPort) - 1)]

                    # Get the username.
                    thisUser = identityList[identityList.index(thisIPAndPort) - 4]

                    # Get the host IP.
#                    tempHost = thisIPAndPort.split(",")
#                    tempHost = tempHost[0]
#                    tempHost = tempHost[2:(len(tempHost) - 1)]
                    
                    # Get the port number for the remote host.
                    i = identityList.index(thisIPAndPort)
                    tempHost = identityList[i - 3]
                    tempPort = identityList[i - 2]

                    # Get the speed for the client.
                    tempSpeed = identityList[identityList.index(thisIPAndPort) - 1]

                    if desc[len(desc)-1] == '':
                        desc.pop()

                    for x in range(len(desc)):
                        if j % 2 == 0:
                            tempFilename = desc[j]
                            thisDesc = tempFilename + ";" + tempHost + ";" + tempPort + ";" + tempSpeed
                            fileDesc.append(thisDesc)
                            author.append(thisUser)
                            j += 1

                        elif j % 2 == 1:
                            fullDesc.append(desc[j])
                            j += 1

                # Closes the connection with the server.
                elif command[0] == "QUIT":

                    # Used to get the ip and port of the current client.
                    thisIPAndPort = str(connection)
                    thisIPAndPort = thisIPAndPort.split("=")
                    thisIPAndPort = thisIPAndPort[len(thisIPAndPort) - 1]
                    thisIPAndPort = thisIPAndPort[0:(len(thisIPAndPort) - 1)]

                    # Removes all traces of the client that is quitting.
                    i = identityList.index(thisIPAndPort)
                    identityList.pop(i)                     # IP
                    thisUser = identityList[i - 4]
                    identityList.pop(i - 1)                 # Speed
                    identityList.pop(i - 2)                 # Remote Port
                    identityList.pop(i - 3)                 # Hostname
                    identityList.pop(i - 4)                 # Username

                    # Loop through all lists to remove this user.
                    x = 0
                    while x < len(author):
                        if thisUser == author[x]:
                            # Remove from all other files.
                            author.remove(author[x])
                            fileDesc.remove(fileDesc[x])
                            fullDesc.remove(fullDesc[x])
                        else:
                            x += 1

                    # Close connection
                    print("Closing connection for", thisUser)
                    allConns.remove(connection)
                    try:
                        connection.close()
                    except Exception:
                        print("Something went wrong closing connection!", Exception)
                    break

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Connection terminated!")
        # if len(allConns) > 0:
        #     for x in allConns:
        #         x.close()
        # sys.exit()


# Starts the connection process with the client.
while True:
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()
    _thread.start_new_thread(clientThread, (connection,))

sock.close()
