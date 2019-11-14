# This is an FTP Server that communicates with an FTP Client. Code was written for CIS 457 at GVSU.
#
# Authors:  Denver DeBoer
#           Nicholas English
#           Kevin Smith
# Date:     10-14-2019


import os
import select
import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverAddress = ('localhost', 10000)
print("Starting on %s port %s" % serverAddress)
sock.bind(serverAddress)
sock.listen(1)

# Starts the connection process with the client.
while (True):
    print("Waiting for a connection...\n")
    connection, clientAddress = sock.accept()

    # Tells the user the connection is successful.
    try:
        print("Connection with ", clientAddress)

        # Listens for the selected input from the client.
        while (True):
            data = connection.recv(1024).decode()
            command = data.split(" ")
            print("Received: %s\n" % data)
            if (data):
                # Displays the list of files in the current directory.
                if (command[0] == "LIST"):

                    fileList = next(os.walk('.'))[2]

                    files = json.dumps({"FILES": fileList})
                    connection.sendall(files.encode())

                # Retrieves a specified file from the current directory.
                elif (command[0] == "RETRIEVE"):
                    try:
                        file = open(command[1], "rb")
                        connection.sendall(file.read(1024))
                        file.close()
                    # If the file doesn't exist, the error will be thrown.
                    except:
                        print('ERROR - Client requested an invalid file.')
                        connection.sendall(''.encode())

                # Tells the server to store a specified file from the client.
                elif (command[0] == "STORE"):
                    print("STORING DATA")
                    file = open(command[1], 'w')
                    totalData = []
                    data = ''

                    # Starts the process for the file to be stored.
                    while (True):
                        ready = select.select([connection], [], [], 2)
                        if (ready[0]):
                            data = connection.recv(1024).decode()
                        else:
                            break
                        totalData.append(data)
                    file.write(''.join(totalData))
                    file.close()
                    print("STORED\n")

                # Closes the connection with the server.
                elif (command[0] == "QUIT"):

                    connection.close()
                    break

                else:
                    print("INVALID COMMAND")
            else:
                break
    finally:
        print("Closing connection")
        connection.close()
