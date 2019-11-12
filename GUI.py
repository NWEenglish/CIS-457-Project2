#GUI
import tkinter
import socket
import select
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connects to central server
#Error checks user input
#Sends username, hostname, and connection speed to server
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
        msg = str(username) + " " + str(hostname) + " " + str(speed)
        sock.sendall(msg.encode())
    else:
        messagebox.showerror("Invalid Input", "Please fill in all fields")

#Keyword Search
#Sends keyword to the central server and displays feedback in modified treeview widget
def keywordSearch():
    key = searchText.get()
    if len(key) > 0:
        sock.sendall(key.encode())
    else:
        messagebox.showerror("Invalid Input", "Please enter in a keyword")

#Connection with Remote Host
#Host can connect, quit, and retrieve files from the remote host
def remoteHost():
    command = ftpText.get()
    if len(command) > 0:
        command = command.split()
        if command[0].upper() == "CONNECT" and len(command) == 3:
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Connecting...\n")
            try:
                ftpAddress = (str(command[1]), int(command[2]))
                sock.connect(ftpAddress)
                ftpResult.insert(tkinter.INSERT, "Connected to " + command[1] + " on port " + command[2] + "\n\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Connection Failed\n\n")
                messagebox.showerror("FTP ERROR", "Could not connect to the server")
        elif command[0].upper() == "RETRIEVE" and len(command) == 2:
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Retrieving File....\n")
            try:
                msg = "RETRIEVE " + command[1]
                sock.sendall(msg.encode())
                
                file = open(command[1], 'w')
                totalData = []
                data = ''
                
                while (True):
                    ready = select.select([sock], [], [], 2)
                    if (ready[0]):
                        data = sock.recv(1024).decode()
                    else:
                        break
                        
                    totalData.append(data)
                    file.write(''.join(totalData))
                    file.close()
                    ftpResult.insert(tkinter.INSERT, "Retrieved " + command[1] + "\n\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Retrieval Failed\n\n")
                messagebox.showerror("FTP ERROR", "Could not retrieve file from the server")
        elif command[0].upper() == "QUIT":
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "Terminating Connection....\n")
            try:
                msg = "QUIT"
                sock.sendall(msg.encode())
                sock.close()
                ftpResult.insert(tkinter.INSERT, "Connection Terminated\n\n")
            except:
                ftpResult.insert(tkinter.INSERT, "Termination Failed\n\n")
                messagebox.showerror("FTP ERROR", "Could not terminate connection to the server")
        elif command[0].upper() == "HELP":
            ftpResult.insert(tkinter.INSERT, "->" + ftpText.get() + "\n")
            ftpResult.insert(tkinter.INSERT, "CONNECT <SERVER NAME/IP ADDRESS> <SERVER PROT>\n")
            ftpResult.insert(tkinter.INSERT, "RETRIEVE <FILENAME>\n")
            ftpResult.insert(tkinter.INSERT, "QUIT\n")
            ftpResult.insert(tkinter.INSERT, "HELP\n\n")
        else:
            messagebox.showerror("Invalid Command", "Please enter a command or type HELP")
    else:
        messagebox.showerror("Invalid Command", "Please enter a command or type HELP")

gui = tkinter.Tk()
gui.title("NAP Host GUI")
gui.geometry("750x525")

##################### CONNECTING TO CENTRAL SERVER ###########################
cLabel = tkinter.Label(gui, text = "Connection", font = ("-weight bold", 13))
cLabel.grid(column = 0, row = 0, padx = 10, sticky = "W", columnspan = 6)

serverHostLabel = tkinter.Label(gui, text = "Server Hostname: ")
serverHostLabel.grid(column = 0, row = 1)
serverHostText = tkinter.Entry(gui, width = 20)
serverHostText.grid(column = 1, row = 1, sticky = "W")

portLabel = tkinter.Label(gui, text = "Port: ")
portLabel.grid(column = 2, row = 1)
portText = tkinter.Entry(gui, width = 6)
portText.grid(column = 3, row = 1, sticky = "W")

connButton = tkinter.Button(gui, text = "Connect", width = 20, command = connectServer)
connButton.grid(column = 4, row = 1, pady = 10, columnspan = 2)

usernameLabel = tkinter.Label(gui, text = "Username: ")
usernameLabel.grid(column = 0, row = 2)
usernameText = tkinter.Entry(gui, width = 15)
usernameText.grid(column = 1, row = 2, sticky = "W")

userHostLabel = tkinter.Label(gui, text = "Hostname: ")
userHostLabel.grid(column = 2, row = 2)
userHostText = tkinter.Entry(gui, width = 20)
userHostText.grid(column = 3, row = 2, sticky = "W")

speedLabel = tkinter.Label(gui, text = "Speed: ")
speedLabel.grid(column = 4, row = 2, padx = 10)
speedOps = ttk.Combobox(gui)
speedOps["values"] = ("Ethernet", "Fiber Optic", "Analog")
speedOps.current(0)
speedOps.grid(column = 5, row = 2, sticky = "W")
##############################################################################

######################### KEYWORD SEARCHING ##################################
sLabel = tkinter.Label(gui, text = "Keyword Search", font = ("-weight bold", 13))
sLabel.grid(column = 0, row = 3, pady = 10, padx = 10, sticky = "W")

searchLabel = tkinter.Label(gui, text = "Search: ")
searchLabel.grid(column = 0, row = 4)
searchText = tkinter.Entry(gui, width = 50)
searchText.grid(column = 1, row = 4, sticky = "W", columnspan = 3)

searchButton = tkinter.Button(gui, text = "Search", width = 20, command = keywordSearch)
searchButton.grid(column = 4, row = 4, columnspan = 2)

searchResult = ttk.Treeview(gui, columns=("hostname", "port", "filename"), height = 5)
searchResult.column("#0", width = 120, minwidth = 120, stretch = tkinter.NO)
searchResult.heading("#0", text="Speed", anchor=tkinter.W)
searchResult.column("hostname", width = 195, minwidth = 195, stretch = tkinter.NO)
searchResult.heading("hostname", text="Hostname", anchor=tkinter.W)
searchResult.column("port", width = 120, minwidth = 120, stretch = tkinter.NO)
searchResult.heading("port", text="Port", anchor=tkinter.W)
searchResult.column("filename", width = 195, minwidth = 195, stretch = tkinter.NO)
searchResult.heading("filename", text="Filename", anchor=tkinter.W)
searchResult.grid(column = 0, row = 5, pady = 10, padx = 20, columnspan = 10, rowspan = 5)
##############################################################################

############################# FTP COMMANDS ###################################
fLabel = tkinter.Label(gui, text = "FTP", font = ("-weight bold", 13))
fLabel.grid(column = 0, row = 10, pady = 10, padx = 10, sticky = "W")

ftpLabel = tkinter.Label(gui, text = "Enter Command: ")
ftpLabel.grid(column = 0, row = 11)
ftpText = tkinter.Entry(gui, width = 50)
ftpText.grid(column = 1, row = 11, sticky = "W", columnspan = 3)

ftpButton = tkinter.Button(gui, text = "Enter", width = 20, command = remoteHost)
ftpButton.grid(column = 4, row = 11, columnspan = 2)

ftpResult = scrolledtext.ScrolledText(gui, width = 75, height = 7)
ftpResult.grid(column = 0, row = 12, pady = 5, padx = 30, columnspan = 6, rowspan = 5)
##############################################################################

gui.mainloop()