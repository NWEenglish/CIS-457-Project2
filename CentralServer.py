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
        allUsers.append(user[0])
        allConns.append(connection)

        identityList.append(user[0])
        identityList.append(str(clientAddress))
        identityList.append(user[2])
        identityList.append(user[3])

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
                    thisUser = identityList[identityList.index(thisIPAndPort) - 1]

                    # Get the host IP.
                    tempHost = thisIPAndPort.split(",")
                    tempHost = tempHost[0]
                    tempHost = tempHost[2:(len(tempHost) - 1)]

                    # Get the port number for the remote host.
                    i = identityList.index(thisIPAndPort)
                    tempPort = identityList[i + 1]

                    # Get the speed for the client.
                    tempSpeed = identityList[identityList.index(thisIPAndPort) + 2]

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
                            author.append(thisUser[0])
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
                    identityList.pop(i + 2)                 # Speed
                    identityList.pop(i + 1)                 # Remote Port
                    identityList.pop(i)                     # IP
                    thisUser = identityList[i - 1]
                    identityList.pop(i - 1)                 # Username

                    # Check if items are in list to begin with.
                    if len(author) > 0:
                        # Remove from all other files.
                        index = author.index(thisUser)
                        author.remove(author[index])
                        allUsers.remove(allUsers[index])
                        fileDesc.remove(fileDesc[index])
                        fullDesc.remove(fullDesc[index])

                    # Close connection*
                    print("Closing connection for ", thisUser)
                    allConns.remove(connection)
                    # connection.close()
                    try:
                        connection.close()
                    except Exception:
                        print(Exception)
                    break

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Closing connection for all devices")
        if len(allConns) > 0:
            for x in allConns:
                x.close()
        sys.exit()


# Starts the connection process with the client.
while True:
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()
    _thread.start_new_thread(clientThread, (connection,))

sock.close()
