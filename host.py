#HOST PROGRAM
import socket
import json
import select

centralSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remoteSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Main
def main():
    try:
        startup()
    finally:
        quit()


# Starts the program execution.
def startup():
    print('\n\nWelcome to NAP HOST\n\n')
    print('Listed below are the commands. Enter \'HELP\' if you forget!')
    helpCommand()
    beginUI()


# User interface
def beginUI():
    command = input(' ~ ')
    command = command.split()

    # Check the input
    if not command:
        pass
    elif command[0].upper() == 'HELP' and len(command) == 1:
        helpCommand()
    elif command[0].upper() == 'CONNECT_SERVER' and len(command) == 3:
        connectServer(command[1], command[2])
    elif command[0].upper() == 'CONNECT' and len(command) == 3:
        connect(command[1], command[2])
    elif command[0].upper() == 'UPLOAD' and len(command) == 2:
        upload(command[1])
    elif command[0].upper() == 'RETRIEVE' and len(command) == 2:
        retrieve(command[1])
    elif command[0].upper() == 'QUIT' and len(command) == 1:
        quitConnection()
    elif command[0].upper() == 'CLOSE' and len(command) == 1:
        return
    else:
        print('\n ERROR - Something went wrong!\n\t Command ' + command[0].upper() + ' caused an error!\n')

    beginUI()


# Prints to the user the available commands.
def helpCommand():
    print('\n\n-------------------- Commands --------------------')
    print('CONNECT_SERVER <SERVER NAME/IP ADDRESS> <SERVER PORT>')
    print('CONNECT <REMOTE HOSTNAME/IP ADDRESS> <REMOTE HOST PORT>')
    print('UPLOAD <FILENAME>')
    print('RETRIEVE <FILENAME>')
    print('QUIT')
    print('HELP')
    print('CLOSE')
    print('--------------------------------------------------\n\n')

#Connect to the central server
#Send host information
def connectServer(serverName, serverPort):
    try:
        print(' Connecting...')

        serverAddress = (str(serverName), int(serverPort))
        centralSock.connect(serverAddress)

        print(' Connected!')
        
        print("Enter username, hostname, and connection speed(Ethernet,T1,etc.)")
        print("<username hostname speed>")
        hostInfo = input(" ~ ")
        centralSock.sendall(hostInfo.encode())

    except:
        print(' ERROR - Could NOT connect to server!')

#Connect to remote host
def connect(serverName, serverPort):
    try:
        print(' Connecting...')

        serverAddress = (str(serverName), int(serverPort))
        remoteSock.connect(serverAddress)

        print(' Connected!')

    except:
        print(' ERROR - Could NOT connect to server!')

#Upload file description file to central server
def upload(filename):
    try:
        print("Uploading file description file...")
        msg = "UPLOAD " + filename
        centralSock.sendall(msg.encode())
        file = open(filename, 'rb')
        centralSock.sendall(file.read(1024))
        print("File Uploaded")
    except:
        print("ERROR - file could not be uploaded")
        
    try:
        file.close()
    except:
        print("ERROR - file could not be closed")

# Requests the server to send the specified file.
def retrieve(filename):
    print(" RETRIEVING DATA...")
    msg = "RETRIEVE " + filename
    remoteSock.sendall(msg.encode())
    file = open(filename, 'w')
    totalData = []
    data = ''

    while (True):
        ready = select.select([remoteSock], [], [], 2)
        if (ready[0]):
            data = remoteSock.recv(1024).decode()
        else:
            break
        totalData.append(data)
        file.write(''.join(totalData))
        file.close()
        print(" DATA RETRIEVED!\n")

# Terminates connection with server.
def quitConnection():
    print(' Terminating connection...')
    try:
        msg = 'QUIT'
        sendMessage(msg)
        remoteSock.close()
    except:
        print(' An error has occurred! This may be caused due to no connection.')

    print(' Connection terminated!')


# Sends the message to the server.
def sendMessage(msg):
    try:
        # print("Sending %s" % msg)
        remoteSock.sendall(msg.encode())
    except:
        print(' ERROR - Request NOT sent to server!')


main()