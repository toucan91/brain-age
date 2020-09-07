import tkinter as tk
from threading import Thread, Event
from tkinter import filedialog, Text
import time
import math
import main
import ans as a

# variables for question
# number of questions
n = 10
# tries per question
tries_limited = False
lim = 5
# list of questions
ls = None
# property of answer
digit = -1
ans = -1
ans_str = ""
# answering or not
foo = False

# thread event flag
result_available = Event()
timer_wait = Event()

# functions

def runThread():
    thread = Thread(target=runApp)
    thread.start()
    
def timer():
    t0 = time.time()
    timer_wait.wait()
    print("Your time is")
    print('%.2f' % (time.time() - t0))
    
def event_handle(event):
    global ans
    global ans_str
    
    global digit
    
    if foo and digit < 0:
        
        canvas.delete("ans")
        
        # answer string
        ans_str += event.char
        
        # answer value
        place = 10 ** -( digit + 1 )
        ans += int(event.char) * place
        
        print("answer is " + str(ans + 1))
        
        # increment digit
        digit += 1
        
        # clean up answer canvas 
        canvas.create_text(250, 50, font=("Purisa", 64), fill="Blue", text=ans_str, tag="ans")
       
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

def render(s = "!", x = 250, y = 250, c="black", d="True"):
    print(s)
    if d:
        canvas.delete('all')
        
    canvas.create_text(x, y, font=("Purisa", 64), fill=c, text=s)

def runApp():
    global ls
    global foo
    global digit
    
    # global variables
    foo = True
    ls = [a.question() for i in range(n)]
    
    # local variables
    n_ = n
    next_q = ls[0]
    correct = 0
    
    # timer
    thread = Thread(target=timer)
    thread.start()
    
    while bool(n_):
        while not next_q.sol:
            render(next_q.ask())
            digit = -1 * next_q.ans_digit()
            tries = lim 
            
            result_available.wait()
            tries -= 1
            
            # get result 
            guess = ans + 1
            
            if tries_limited and tries == 0:
                render(":O out of tries, by the way it's " + str(next_q.ans))
                guess = next_q.ans
            
            time.sleep(0.2)
            
            if guess == next_q.ans:
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

    
    foo = False
    timer_wait.set()
    
    canvas.delete('all')
    t = "Answered " + str(correct) + " questions correctly!"
    canvas.create_text(250, 250, font=("Purisa", 11), fill="red", text=t)
    t = str('%.2f' % (100 * correct / n)) + " % accurary"
    canvas.create_text(250, 270, font=("Purisa", 11), fill="red", text=t)
    
    foo = False

# make window
root = tk.Tk()

canvas = tk.Canvas(root, height = 500, width = 500, bg="white")
canvas.pack()
canvas.focus_set()

for i in range(10):
    canvas.master.bind(str(i), event_handle)

runApps = tk.Button(root, text = "Run Apps", padx=20, pady=5, fg="white", bg="#263D42", command=runThread)
runApps.pack()

'''
inc = tk.Button(root, text = "Increment", padx=20, pady=5, fg="white", bg="#263D42", command=inc)
inc.pack()
'''

root.mainloop()
