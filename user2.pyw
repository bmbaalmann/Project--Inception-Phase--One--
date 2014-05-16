# import libraries needed
import thread
from mychat import *

# basic requirements to run the chat program
# title of the window
WindowTitle = 'User number Two'
s = socket(AF_INET, SOCK_STREAM)
HOST = gethostname()
PORT = 8011
# the IP address of my local machine
conn = '10.63.236.84'
s.bind((HOST, PORT))

# mouse function
def ClickAction():
    # message to chat window
    EntryText = FilteredMessage(EntryBox.get("0.0",END))
    LoadMyEntry(ChatLog, EntryText)
    ChatLog.yview(END)
    EntryBox.delete("0.0",END)
    conn.sendall(EntryText)
    
# keyboard function
def PressAction(event):
	EntryBox.config(state=NORMAL)
	ClickAction()
def DisableEntry(event):
	EntryBox.config(state=DISABLED)

# GUI function

# create a window
base = Tk()
base.title(WindowTitle)
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

# chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.insert(END, "Waiting on user to join\n")
ChatLog.config(state=DISABLED)

# scrollbar on the window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# send button
SendButton = Button(base, font=30, text="Send", width="8", height=5,
                    bd=0, bg="#ffb6c1", activebackground="#ffb6c1",
                    command=ClickAction)

# message box
EntryBox = Text(base, bd=0, bg="white",width="20", height="3", font="Arial")
EntryBox.bind("<Return>", DisableEntry)
EntryBox.bind("<KeyRelease-Return>", PressAction)

# message box parameters
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

# connection function

def GetConnected():
    s.listen(1)
    global conn
    conn, addr = s.accept()
    LoadConnectionInfo(ChatLog, 'Connected ' + str(addr) + '\n---------------------------------------------------------------')
    
    while 1:
        try:
            data = conn.recv(1024)
            LoadOtherEntry(ChatLog, data)
            if base.focus_get() == None:
                FlashMyWindow(WindowTitle)
                playsound('chime_up.wav')
        except:
            LoadConnectionInfo(ChatLog, '\n [ User has disconnected ]\n [ Waiting for him to connect..] \n  ')
            GetConnected()

    conn.close()
    
thread.start_new_thread(GetConnected,())

base.mainloop()


