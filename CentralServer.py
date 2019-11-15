# Central Server
import socket
import _thread

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

def clientThread(connection):
    # Tells the user the connection is successful.
    try:

        # Gets the user that connected and add to user table
        user = connection.recv(1024).decode()
        user = user.split(" ")
        allUsers.append(user[0])
        print("Connection with ", clientAddress)
        print("    User: ", user[0])

        # Listens for the selected input from the client.
        while (True):
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("Received: %s\n" % data)
            if (data):

                # Do a keyword search.
                if (command[0] == "KEYWORD_SEARCH"):
                    term = command[1]
                    whoHasTerm = []
                    foundWho = ""

                    whoHasTerm = ";".join(s for s in fullDesc if term.lower() in s.lower())
                    whoHasTerm = whoHasTerm.split(";")

                    for x in whoHasTerm:
                        foundWho += fileDesc[fullDesc.index(x)] + ";"

                    connection.sendall(foundWho.encode())

                # Get a file description.
                elif (command[0] == "FILE_DESC"):
                    j = 0

                    desc = connection.recv(1024).decode()
                    desc = desc.split(";")

                    if desc[len(desc)-1] == '':
                        desc.pop()

                    for x in range(len(desc)):
                        if j % 2 == 0:
                            tempFilename = desc[j]
                            tempHost = user[1]
                            tempPort = user[2]
                            tempSpeed = user[3]
                            thisDesc = tempFilename + ";" + tempHost + ";" + tempPort + ";" + tempSpeed
                            fileDesc.append(thisDesc)
                            author.append(user[0])
                            j += 1

                        elif j % 2 == 1:
                            fullDesc.append(desc[j])
                            author.append(user[0])
                            j += 1

                # Closes the connection with the server.
                elif (command[0] == "QUIT"):

                    for x in author:
                        index = author.index(user[0])
                        author.remove(author[index])
                        allUsers.remove(allUsers[index])
                        fileDesc.remove(fileDesc[index])
                        fullDesc.remove(fullDesc[index])

                    # Close connection*
                    connection.close()
                    break

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Closing connection")
        connection.close()
        return

# Starts the connection process with the client.
while (True):
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()
    _thread.start_new_thread(clientThread, (connection,))

sock.close()
