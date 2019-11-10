#GUI
import tkinter
import socket
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connects to server
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
        messagebox.showinfo("Connection", "Connected to Central Server")
        msg = str(username) + " " + str(hostname) + " " + str(speed)
        sock.sendall(msg.encode())
    else:
        messagebox.showerror("Invalid Input", "Please Fill In All Fields")


gui = tkinter.Tk()
gui.title("NAP Host GUI")
gui.geometry("700x525")

##################### CONNECTING TO CENTRAL SERVER ###########################
cLabel = tkinter.Label(gui, text = "Connection", font = "bold")
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
sLabel = tkinter.Label(gui, text = "Keyword Search", font = "bold")
sLabel.grid(column = 0, row = 3, pady = 15, padx = 10, sticky = "W")

searchLabel = tkinter.Label(gui, text = "Search: ")
searchLabel.grid(column = 0, row = 4)
searchText = tkinter.Entry(gui, width = 50)
searchText.grid(column = 1, row = 4, sticky = "W", columnspan = 3)

searchButton = tkinter.Button(gui, text = "Search", width = 20)
searchButton.grid(column = 4, row = 4, columnspan = 2)

searchResult = scrolledtext.ScrolledText(gui, width = 75, height = 7)
searchResult.grid(column = 0, row = 5, pady = 10, padx = 30, columnspan = 6, rowspan = 5)
##############################################################################

############################# FTP COMMANDS ###################################
fLabel = tkinter.Label(gui, text = "FTP", font = "bold")
fLabel.grid(column = 0, row = 10, pady = 15, padx = 10, sticky = "W")

ftpLabel = tkinter.Label(gui, text = "Enter Command: ")
ftpLabel.grid(column = 0, row = 11)
ftpText = tkinter.Entry(gui, width = 50)
ftpText.grid(column = 1, row = 11, sticky = "W", columnspan = 3)

ftpButton = tkinter.Button(gui, text = "Enter", width = 20)
ftpButton.grid(column = 4, row = 11, columnspan = 2)

ftpResult = scrolledtext.ScrolledText(gui, width = 75, height = 7)
ftpResult.grid(column = 0, row = 12, pady = 5, padx = 30, columnspan = 6, rowspan = 5)
##############################################################################

gui.mainloop()