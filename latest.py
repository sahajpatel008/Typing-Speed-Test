import random
import re
import numpy as np
from tkinter import *
from tkinter import messagebox
from matplotlib import pyplot as plt
from PIL import ImageTk, Image
 
displaystring = ""
inputstring = ""
# TIME=15
TIME=60
timeleft = TIME
PRIMARY_COLOR = "#354344"
# SECONDARY_COLOR = "#EF7D13"
SECONDARY_COLOR = "#00ffff"
 
with open ('100words.txt') as f:
    word_list = f.read().split(" ")
 
#new window for graph 
 
def plot():
    errorList = []
    wpmList = []
    attemptList = []
    
    with open("records.txt", "r") as f:
        content = f.read().splitlines()
        for i in range(len(content)):
            content_split = content[i].split(',')
            attemptList.append(i+1)
            wpmList.append(float(content_split[0]))
            errorList.append(float(content_split[1]))
                
    # print(attemptList)
    # print(wpmList)
    # print(errorList)
 
    plt.plot(np.array(attemptList), np.array(wpmList), color="green", marker='.')
    plt.plot(np.array(attemptList), np.array(errorList), color="red", marker='.')
    plt.xlabel("Attempt")
    plt.title("Graph")
    plt.legend(["WPM", "Error"], loc ="best")
    plt.show()
 
root = Tk()
root.title("Typing Speed Test")
root.geometry("900x600")
root.resizable(0, 0)
 
#time function 
 
def time():
    global timeleft
    global inputstring
    global displaystring
    
   
    # if(timeleft >= 11):
   
 
    # 60 second 
    if timeleft >= 58:
        time_label.configure(fg="black")
        inputstring = ""
    elif timeleft >= 11: 
        pass
    else:
        time_label.configure(fg="red")
 
    if timeleft>0:
        timeleft -= 1
        time_label.configure(text=timeleft)
        time_label.after(1000, time)
    else:
        L.config(text="TIME UP!")
        
        print(word_entry.get())
        inputstring += word_entry.get()
 
        inputstring = inputstring.strip()
        displaystring = displaystring.strip()
 
        inputstring = re.sub(' +', ' ', inputstring)
        displaystring = re.sub(' +', ' ', displaystring)
 
        print("Final:",inputstring, sep="")
        print("Display:",displaystring, sep="")
 
        wpm = (len(inputstring)/5)/(TIME/60)
 
        wrongchar = 0
 
        inputlist = inputstring.split(" ")
        displaylist = displaystring.split(" ")
 
        for i in range(min(len(inputlist), len(displaylist))):
            if inputlist[i] != displaylist[i]:
                
                # wrongchar += len(displaylist[i])
                for j in range(min(len(inputlist[i]), len(displaylist[i]))):
                    if inputlist[i][j]!=displaylist[i][j]:
                        wrongchar+=1
 
        print("Gross:", wpm)
        print(wrongchar)
 
        net = wpm - wrongchar/TIME
 
        print("Net:", net)
 
        accuracy = ((len(inputstring)-wrongchar)/len(inputstring))*100
        print("Accuracy:", accuracy)
        
        word_entry.config(state= "disabled")
 
        # AccuLabel.config(text=f"Speed: {net}WPM\tAccuracy: {accuracy}%", foreground=SECONDARY_COLOR)
        AccuLabel.config(text="Speed: {0:5.2f} WPM\tAccuracy: {1:5.2f}%".format(net,accuracy), foreground="white")
        # word_entry.delete(0, END)
        rr = messagebox.askyesno('Notification', 'Do you want to play again?') #show notificatinon when time is over
        # word_entry.delete(0, END)
 
        with open("records.txt", "a") as f:
            f.write(f"{net},{wrongchar}\n")
 
        if rr == True:
            word_entry.delete(0, END)
            displaystring = ""
            timeleft = TIME
            time_label.configure(text=timeleft)
            temstr = " ".join(random.sample(word_list, 12))
            L.configure(text=temstr)
            word_entry.config(state = "normal")
            L.config(text="Press Enter to Start")
            inputstring = ""
               
        else :
            # openwindow()
            plot()
 
def startGame(event):
    global inputstring
    global displaystring
 
    # inputstring = ""
    # displaystring = ""
 
    if timeleft==TIME:
        time()
 
    if timeleft <= 0:
        # L.configure(text="TIMES UP")
        # word_entry.delete(0,END)
        word_entry.config(state="disabled")
        # print(inputstring)
    
    # print(word_entry.get())
    inputstring += word_entry.get()
    inputstring += " "
 
    # random.shuffle(word_list)
    temstr = " ".join(random.sample(word_list, 12))
    displaystring += (temstr + " ")
    
    L.configure(text=temstr)  
    word_entry.delete(0,END)
 
#frame1
f1 = Frame(root, height=200, width=900, pady=10, bg=PRIMARY_COLOR)
f1.pack(fill=X)
Label(f1, text="TYPING SPEED TEST", width=0, padx=85, font="Georgia 50 bold", foreground=SECONDARY_COLOR, background=PRIMARY_COLOR).grid(row=0, column=0)
 
# Image Frame
image = ImageTk.PhotoImage(Image.open(r'image.png'))

icon = ImageTk.PhotoImage(Image.open(r'icon2.jpg'))
root.iconphoto(False, icon)

 
 
iLabel = Label(root, text='', image=image, compound='center', background=PRIMARY_COLOR)
iLabel.pack(fill=X)
 
#frame2
f2 = Frame(root, height=200, width=900, pady=10, bg=PRIMARY_COLOR) 
# f2.pack_propagate(0)
f2.pack()
# f2.pack(fill=X)
 
# random.shuffle(word_list) #re-arrange list
L = Label(f2, bg="WHITE", text="Press Enter to Start", width = 200, padx=25, font="Calibri 25 bold", foreground="white", background=PRIMARY_COLOR)
L.pack()
 
#input
f3 = Frame(root, height=50, width=800, pady=10, background=PRIMARY_COLOR)
f3.pack_propagate(0)
# f3.pack()
f3.pack(fill=X)
# --> input text 
word_entry = Entry(root,width=100,font="Calibri 25")
# word_entry.grid(row=0,column=0,ipady=10)  
# word_entry.focus_set()
word_entry.pack(padx=10)
 
l = Label(f3, text="Time Left:",bg="light blue", font="Ubuntu 15 bold")
l.pack()
#time label:
time_label = Label(f3, text=timeleft,bg="light blue", font="Ubuntu 15 bold")
time_label.grid(row=0,column=1, padx=500)
# time_label.pack()
 
f4 = Frame(root, height=200, width=900, pady=10, bg=PRIMARY_COLOR)
f4.pack()
AccuLabel = Label(f4, background=PRIMARY_COLOR,text="", width=200, padx=25, font="Ubuntu 25 bold")
AccuLabel.pack()
  
f5 = Frame(bg=PRIMARY_COLOR)
# f4.pack_propagate(0)
f5.pack(fill=X)
 
bt = Button(f5, text="Show Graph",command = plot, font="Ubuntu 15 bold", background=SECONDARY_COLOR, relief=RAISED)
bt.pack()
 
 
root.bind('<Return>',startGame) #bind enter button: click enter
 
 
def run():
    root.mainloop()
 
if __name__ == '__main__':
    run()