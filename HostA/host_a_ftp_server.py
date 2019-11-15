# This is an FTP Server that communicates with an FTP Client. Code was written for CIS 457 at GVSU.
#
# Authors:  Denver DeBoer
#           Nicholas English
#           Kevin Smith
# Date:     10-14-2019

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverAddress = ('localhost', 16141)
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
                # Retrieves a specified file from the current directory.
                if (command[0] == "RETRIEVE"):
                    try:
                        file = open(command[1], "rb")
                        connection.sendall(file.read(1024))
                        file.close()
                    # If the file doesn't exist, the error will be thrown.
                    except:
                        print('ERROR - Client requested an invalid file.')
                        connection.sendall(''.encode())

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
