import tkinter as tk
from threading import Thread, Event
from tkinter import filedialog, Text

import time
import math
import numpy as np
from skimage.transform import resize

import knn
import ans as a

##############################
# window sizes
w = h = 28*16

# variables for question
n = 10

# tries per question
triesLimited = True
limit = 1

# list of questions
ls = None

# property of answer
digit = -1
ans = -1
ans_str = ""
ansDraw = -1

# answering state
foo = False

# last mouse 
lastx = None
lasty = None

# option to draw number 
# 0 ----- when not inputing answer via drawing
answerState = 0

# drawing matrix
dLength = h
draw = np.zeros((dLength,dLength))

# model
knn = knn.knnGuessNumber()
k = 8
###############################

# thread event flag
result_available = Event()
timer_wait = Event()

################################
# functions

def runThread():
    if not foo:
        thread = Thread(target=runApp)
        thread.start()
        
    
def timer():
    t0 = time.time()
    timer_wait.wait()
    string = "Your time is " + str(round(time.time() - t0 , 2)) + " seconds"
    
    canvas.create_text(w/2, h/2 - 80, font=("Purisa", 11), fill="red", text=string)
    
def event_handle(event):
    global ans
    global ans_str
    global w
    global digit
    
    if foo and digit < 0:
        
        canvas.delete("ans")
        
        # read input string
        ans_str += event.char
        
        # shift string value
        place = 10 ** -( digit + 1 )
        ans += int(event.char) * place
        
        print("answer is " + str(ans + 1))
        
        # increment digit
        digit += 1
        
        # clean up answer canvas 
        canvas.create_text(w/2, 50, font=("Purisa", 64), fill="Blue", text=ans_str, tag="ans")
       
        # return to thread
        if digit == 0:
            result_available.set()
            

def cleanUp(question):
    global ans 
    global ans_str
    
    # set flag
    result_available.clear() 
    
    # reset values 
    ans = -1
    ans_str = ""
    
    # clean up answer canvas
    canvas.delete("ans")

def render(s = "!", x = 224, y = 224, c="black", d="True"):
    if d:
        canvas.delete('all')
        
    canvas.create_text(x, y, font=("Purisa", 64), fill=c, text=s)

def runApp():
    global ls
    global foo
    global digit
    global w
    
    
    foo = True
    canvas.delete('all')
    
    # global variables
    ls = [a.question() for i in range(n)]
    updateMax(None)
    
    # local variables
    n_ = n
    next_q = ls[0]
    correct = 0
    
    # timer
    thread = Thread(target=timer)
    thread.start()
    
    while bool(n_):
    
        tries = limit
            
        while not next_q.sol:
            
            render(next_q.ask())
            digit = -1 * next_q.ans_digit()
            tries -= 1
            
            if triesLimited and tries < 0:
                render("skip")
                
                time.sleep(0.4)
                
                next_q.solve()
                break
            
            result_available.wait()
            
            # get result 
            guess = ans + 1
            guessDraw = ansDraw
            
            time.sleep(0.2)
            
                    
            if guess == next_q.ans or guessDraw == next_q.ans:
                correct += 1
                # clean up 
                cleanUp(next_q)
                next_q.solve()
                
            else:
                time.sleep(0.2)
            
                # clean up 
                cleanUp(next_q)
            

            
        # goto next question
        n_ -= 1
        next_q = ls[-n_]

    
    timer_wait.set()
    
    canvas.delete('all')
    t = "Answered " + str(correct) + " questions correctly! out of " + str(n)
    canvas.create_text(w/2, h/2, font=("Purisa", 11), fill="red", text=t)
    t = str('%.2f' % (100 * correct / n)) + " % accurary"
    canvas.create_text(w/2, h/2+ 40, font=("Purisa", 11), fill="red", text=t)
    
    foo = False

def limitTriesSwitch():
    global triesLimited
    
    if triesLimited:
        limitTries.config(text = "Limit Tries/Question" )
        sliderTries.configure(state='normal')
        updateLimit()
    else:
        limitTries.config(text = "No Limit")
        sliderTries.configure(state='disabled')
        
    triesLimited = not triesLimited
    

def updateLimit(event=None):
    global limit
    
    if triesLimited and not foo:
        s_val = sliderTries.get()
        limit = int(s_val)
        

def updateMax(event=None):
    global n
    
    if not foo:
        s_val = slider.get()
        n = int(s_val)
        t = "Max Questions = " + str(n) 
        maxQuestion.config(text = t )
        
def xyPos(event):
    global answerState
    global lastx, lasty
    "Takes the coordinates of the mouse when you click the mouse"
    if answerState:
        lastx, lasty = event.x, event.y
    
def addLine(event):
    global answerState
    global lastx, lasty
    #global draw
    if answerState:
        valWidth = 16.0
        scale = int(1.5*valWidth)
        canvasDraw.create_line((lastx, lasty, event.x, event.y), width=valWidth, smooth=1, splinesteps=30)
        # fill in square around cord
        for i in range(0,scale):
            for j in range(0,scale):
                if (event.x - i) >= 0 and (event.x - i) <= w - 1 and event.y + j <= w - 1 and event.y + j >= 0:
                    draw[event.x - i, event.y + j] = 1
                if (event.x - i) >= 0 and (event.x - i) <= w - 1 and event.y - j <= w - 1 and event.y - j >= 0:
                    draw[event.x - i, event.y - j] = 1
                if (event.x + i) >= 0 and (event.x + i) <= w - 1 and event.y + j <= w - 1 and event.y + j >= 0:
                    draw[event.x + i, event.y + j] = 1
                if (event.x + i) >= 0 and (event.x + i) <= w - 1 and event.y - j <= w - 1 and event.y - j >= 0:
                    draw[event.x + i, event.y - j] = 1
                    
        # this makes the new starting point of the drawing
        lastx, lasty = event.x, event.y
        
def clearDraw():
    global draw
    draw = np.zeros((dLength, dLength))
    canvasDraw.delete('all')
    
def handelDrawing():
    global ansDraw
    global draw
    
    l = None
    k = int(sliderk.get())
        
    if foo:
        if digit > 1:
            # process draw matrix
            # use draw matrix to predict answer 
            d1 = np.ravel(resize(draw[:,0:int((28*16)/2 - 1)], (28,28)))
            d2 = np.ravel(resize(draw[:,int((28*16)/2):int((28*16) - 1)], (28,28)))
            ansDraw, l = 10*knn.KNN(d1,k) + knn.KNN(d2,k)
        else:
            # use draw matrix to predict answer 
            newimg = np.ravel(resize(draw, (28,28), anti_aliasing=True))
            ansDraw, l = knn.KNN(newimg, k)
            
            
        result_available.set()
            
    else:
        
    
        # use draw matrix to predict answer 
        newimg = resize(draw, (28,28))
        # save canvas
        with open('outfile.txt', 'wb') as f:
            for row in newimg:
                np.savetxt(f, row, fmt='%.2f')
        
        newimg = np.ravel(newimg)
        ansDraw, l = knn.KNN(newimg, k)
        
        t = "hmm.. No questions to answer"
        canvas.delete('all')
        canvas.create_text(w/2, w/2, font=("Purisa", 11), fill="red", text=t)
    
    
    clearDraw()
    guess = "My guess is " + str(ansDraw)
    canvasDraw.create_text(dLength/2, dLength/2, font=("Purisa", 11), fill="black", text=guess)
        
         
def answerDrawing():
    global answerState
    # not answering questions, change to ready for drawing
    if answerState == 0:
        clearDraw()
        answerState = 1
        answerButton['text'] = "End"
        
    # done answering, process drawing and guess
    else:
        handelDrawing()
        answerState = 0
        answerButton.config(text="Draw Number")
        

    
# make window
root = tk.Tk()

# create frame
topFrame = tk.Frame(root)
topFrame.pack()
topFrame.pack_propagate(False)

botFrame = tk.Frame(root)
botFrame.pack(side=tk.RIGHT)
botFrame.pack_propagate(False)

# blank background
canvas = tk.Canvas(root, height = h, width = w, bg="white")
canvas.pack(side="left", fill="both", expand=True)
canvas.focus_set()
canvasDraw = tk.Canvas(root, height = dLength, width = dLength, bg="grey")
canvasDraw.pack(side="right", fill="both", expand=False)

# handle number keyboard input
for i in range(10):
    canvas.master.bind(str(i), event_handle)

# run question 
runApps = tk.Button(botFrame, text = "Run Apps", padx=20, pady=5, fg="white", bg="#263D42", command=runThread)
runApps.grid(column=0, row =0)

# label number of questions
maxQuestion = tk.Button(botFrame, text = "Max Questions = " + str(n), padx=20, pady=5, fg="white", bg="#263D42", state=tk.DISABLED)
maxQuestion.grid(column=0,row=1)


# slider for number of questions 
slider = tk.Scale(botFrame, from_=1, to=50, orient="horizontal")
slider.set(n)
slider.bind("<ButtonRelease-1>", updateMax)
slider.grid(column=0,row=2)

# limit tries 
limitTries = tk.Button(botFrame, text = "Limit Tries/Question", padx=20, pady=5, fg="white", bg="#263D42", command=limitTriesSwitch)
limitTries.grid(column=0,row=3)

# slider for number of tries 
sliderTries = tk.Scale(botFrame, from_=1, to=50, orient="horizontal")
sliderTries.set(limit)
sliderTries.bind("<ButtonRelease-1>", updateLimit)
sliderTries.grid(column=0,row=4)

# drawing answer
canvasDraw.bind("<Button-1>", xyPos)
canvasDraw.bind("<B1-Motion>", addLine)

# clear
ansButtonText = "Draw Number"
answerButton = tk.Button(botFrame, text=ansButtonText, command=answerDrawing)
answerButton.grid(column=0,row=5)
clear = tk.Button(botFrame, text="Clear Drawing", command=clearDraw)
clear.grid(column=0,row=6)

# knn
setK = tk.Button(botFrame, text="Set k in KNN model", bg="#263D42", state=tk.DISABLED)
setK.grid(column=0,row=7)

sliderk = tk.Scale(botFrame, from_=1, to=40, orient="horizontal")
sliderk.set(k)
sliderk.grid(column=0,row=8)


root.mainloop()

