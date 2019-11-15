# GUI
import tkinter
import socket
import select
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
remoteSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connects to central server
# Error checks user input
# Sends username, hostname, and connection speed to server
def connectServer():
    servIP = serverHostText.get()
    port = portText.get()
    username = usernameText.get()
    hostname = userHostText.get()
    speed = speedOps.get()

    if len(servIP) > 0 and len(port) > 0 and len(username) > 0 and len(hostname) > 0 and len(speed) > 0:
        serverAddress = (str(servIP), int(port))
        sock.connect(serverAddress)
        messagebox.showinfo("Connection", "Connected to central server")

        msg = str(username) + " " + str(hostname) + " " + str(16242) + " " + str(speed)
        sock.sendall(msg.encode())

        disButton["state"] = tkinter.NORMAL
        connButton["state"] = tkinter.DISABLED
    else:
        messagebox.showerror("Invalid Input", "Please fill in all fields")


# Browse for a description file
def browse():
    description = tkinter.filedialog.askopenfilename()
    filepathText.insert(0, description)


# File Description Upload
def shareFile():
    path = filepathText.get()

    if len(path) > 0:
        try:
            msg = "FILE_DESC " + path
            sock.sendall(msg.encode())
            file = open(path, "rb")                            # ---------------------------------------------------------------------------------
            sock.sendall(file.read(1024))
            messagebox.showinfo("File Description", "Description file successfully uploaded")
        except:
            messagebox.showerror("File Error", "Description file failed to upload")
    else:
        messagebox.showerror("File Error", "Description file not found")


# Disconnect from the central server
def disconnect():
    try:
        msg = "QUIT"
        sock.sendall(msg.encode())
        sock.close()
        messagebox.showinfo("Disconnection", "Disconnected from central server")
        connButton["state"] = tkinter.NORMAL
        disButton["state"] = tkinter.DISABLED
    except:
        messagebox.showerror("ERROR", "Failure to disconnect from central server")


# Keyword Search
# Sends keyword to the central server and displays feedback in modified treeview widget
def keywordSearch():
    key = searchText.get()
    totalData = []
    dataArray = []
    i = 0
    j = 0

    if len(key) > 0:

        # Clear table
        for x in searchResult.get_children():
            searchResult.delete(x)
                
        msg = "KEYWORD_SEARCH " + key
        sock.sendall(msg.encode())

        while (True):
            ready = select.select([sock], [], [], 2)
            if (ready[0]):
                data = sock.recv(1024).decode()
            else:
                break
            totalData.append(data)

            # Extract Data
            dataArray = totalData[0].split(";")

            if dataArray[len(dataArray) - 1] == '':
                dataArray.pop()

            print(dataArray)

        while (j < (( len(dataArray) ) / 4) ):
            searchResult.insert("", j + 1, text=dataArray[i], values=(dataArray[i + 1], dataArray[i + 2], dataArray[i + 3]))
            j += 1
            i += 4
    else:
        messagebox.showerror("Invalid Input", "Please enter in a keyword")


# Connection with Remote Host
# Host can connect, quit, and retrieve files from the remote host
def remoteHost():
    command = ftpText.get()
    if len(command) > 0:
        command = command.split()
        if command[0].upper() == "CONNECT" and len(command) == 3:
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Connecting...\n")
            try:
                ftpAddress = (str(command[1]), int(command[2]))
                remoteSock.connect(ftpAddress)
                ftpResult.insert(tkinter.INSERT, "Connected to " + command[1] + " on port " + command[2] + "\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Connection Failed\n")
                messagebox.showerror("FTP ERROR", "Could not connect to the server")
        elif command[0].upper() == "RETRIEVE" and len(command) == 2:
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Retrieving File....\n")
            try:
                msg = "RETRIEVE " + command[1]
                remoteSock.sendall(msg.encode())

                file = open(command[1], 'w')
                data = ''

                while (True):
                    ready = select.select([remoteSock], [], [], 2)
                    if (ready[0]):
                        data = remoteSock.recv(1024)
                        file.write(data)
                    else:
                        break
                file.close()
                ftpResult.insert(tkinter.INSERT, "Retrieved " + command[1] + "\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Retrieval Failed\n")
                messagebox.showerror("FTP ERROR", "Could not retrieve file from the server")
        elif command[0].upper() == "QUIT":
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Terminating Connection....\n")
            try:
                msg = "QUIT"
                remoteSock.sendall(msg.encode())
                remoteSock.close()
                ftpResult.insert(tkinter.INSERT, "Connection Terminated\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Termination Failed\n")
                messagebox.showerror("FTP ERROR", "Could not terminate connection to the server")
        elif command[0].upper() == "HELP":
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "CONNECT <SERVER NAME/IP ADDRESS> <SERVER PROT>\n")
            ftpResult.insert(tkinter.INSERT, "RETRIEVE <FILENAME>\n")
            ftpResult.insert(tkinter.INSERT, "QUIT\n")
            ftpResult.insert(tkinter.INSERT, "HELP\n")
        else:
            messagebox.showerror("Invalid Command", "Please enter a command or type HELP")
    else:
        messagebox.showerror("Invalid Command", "Please enter a command or type HELP")


gui = tkinter.Tk()
gui.title("NAP Host GUI")
gui.geometry("750x525")

##################### CONNECTING TO CENTRAL SERVER ###########################
cLabel = tkinter.Label(gui, text="Connection", font=("-weight bold", 13))
cLabel.grid(column=0, row=0, padx=10, sticky="W", columnspan=6)

serverHostLabel = tkinter.Label(gui, text="Server Hostname: ")
serverHostLabel.grid(column=0, row=1)
serverHostText = tkinter.Entry(gui, width=25)
serverHostText.grid(column=1, row=1, sticky="W")

portLabel = tkinter.Label(gui, text="Port: ")
portLabel.grid(column=2, row=1)
portText = tkinter.Entry(gui, width=6)
portText.grid(column=3, row=1, sticky="W")

connButton = tkinter.Button(gui, text="Connect", width=10, command=connectServer)
connButton.grid(column=4, row=1, pady=10, padx=5)

disButton = tkinter.Button(gui, text="Disconnect", width=10, command=disconnect)
disButton["state"] = tkinter.DISABLED
disButton.grid(column=5, row=1, pady=10, padx=5)

usernameLabel = tkinter.Label(gui, text="Username: ")
usernameLabel.grid(column=0, row=2)
usernameText = tkinter.Entry(gui, width=15)
usernameText.grid(column=1, row=2, sticky="W")

userHostLabel = tkinter.Label(gui, text="Hostname: ")
userHostLabel.grid(column=2, row=2)
userHostText = tkinter.Entry(gui, width=25)
userHostText.grid(column=3, row=2, sticky="W")

speedLabel = tkinter.Label(gui, text="Speed: ")
speedLabel.grid(column=4, row=2, padx=10)
speedOps = ttk.Combobox(gui, width=10)
speedOps["values"] = ("Ethernet", "Fiber Optic", "Analog")
speedOps.current(0)
speedOps.grid(column=5, row=2, sticky="W")

filepathLabel = tkinter.Label(gui, text="File Description Pathway: ")
filepathLabel.grid(column=0, row=3)
filepathText = tkinter.Entry(gui, width=50)
filepathText.grid(column=1, row=3, columnspan=5, sticky="W")

browseFile = tkinter.Button(gui, text="Browse", width=10, command=browse)
browseFile.grid(column=4, row=3, pady=10, padx=5)

sendFile = tkinter.Button(gui, text="Send", width=10, command=shareFile)
sendFile.grid(column=5, row=3, pady=10, padx=5)
##############################################################################

######################### KEYWORD SEARCHING ##################################
sLabel = tkinter.Label(gui, text="Keyword Search", font=("-weight bold", 13))
sLabel.grid(column=0, row=4, pady=5, padx=10, sticky="W")

searchLabel = tkinter.Label(gui, text="Search: ")
searchLabel.grid(column=0, row=5)
searchText = tkinter.Entry(gui, width=50)
searchText.grid(column=1, row=5, sticky="W", columnspan=3)

searchButton = tkinter.Button(gui, text="Search", width=20, command=keywordSearch)
searchButton.grid(column=4, row=5, columnspan=2)

searchResult = ttk.Treeview(gui, columns=("hostname", "port", "speed"), height=4)
searchResult.column("#0", width=195, minwidth=195, stretch=tkinter.NO)
searchResult.heading("#0", text="Filename", anchor=tkinter.W)
searchResult.column("hostname", width=195, minwidth=195, stretch=tkinter.NO)
searchResult.heading("hostname", text="Hostname", anchor=tkinter.W)
searchResult.column("port", width=120, minwidth=120, stretch=tkinter.NO)
searchResult.heading("port", text="Port", anchor=tkinter.W)
searchResult.column("speed", width=120, minwidth=120, stretch=tkinter.NO)
searchResult.heading("speed", text="Speed", anchor=tkinter.W)
searchResult.grid(column=0, row=6, pady=10, padx=20, columnspan=10, rowspan=5)
##############################################################################

############################# FTP COMMANDS ###################################
fLabel = tkinter.Label(gui, text="FTP", font=("-weight bold", 13))
fLabel.grid(column=0, row=11, pady=5, padx=10, sticky="W")

ftpLabel = tkinter.Label(gui, text="Enter Command: ")
ftpLabel.grid(column=0, row=12)
ftpText = tkinter.Entry(gui, width=50)
ftpText.grid(column=1, row=12, sticky="W", columnspan=3)

ftpButton = tkinter.Button(gui, text="Enter", width=20, command=remoteHost)
ftpButton.grid(column=4, row=12, columnspan=2)

ftpResult = scrolledtext.ScrolledText(gui, width=75, height=7)
ftpResult.grid(column=0, row=13, pady=5, padx=30, columnspan=6, rowspan=5)
##############################################################################

gui.mainloop()