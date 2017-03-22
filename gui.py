from Tkinter import *
from PIL import Image, ImageTk

import vote
import logging

def init():
    logging.info("Initiating GUI")
    global window
    window = Tk()

    global captcha_img
    captcha_img = Label(window)
    captcha_img.pack(side = "top", fill = "both", expand = "yes")

    global email
    email = Entry(window)
    email.insert(0,"your@email.de")
    email.pack()

    global captcha
    captcha = Entry(window)
    captcha.bind("<Return>", vote.enter)
    captcha.pack()
    
    global info
    info = Label(window, text="0 0 0 0 0")
    info.pack()

    global counter_label
    counter_label = Label(window, text="Successful votes: 0")
    counter_label.pack()
    
    global counter
    counter = 0
    logging.info("Successful initiated GUI")

def start():
    email.focus()
    email.selection_range(0, END)
    window.mainloop()
    
def send():
    logging.info("GUI received SEND")
    info.configure(text="SENT")
    info.update()
    
def success():
    logging.info("GUI received SUCCESS")
    info.configure(text="Vote successful!")
    info.update()
    global counter
    counter += 1
    counter_label.configure(text= "Successful votes: " + str(counter))
    counter_label.update()

def error():
    logging.error("GUI received ERROR")
    info.configure(text="ERROR")
    info.update()
        
def reset():
    logging.info("Resetting GUI")
    info.configure(text="Enter CapKey")
    info.update()
    img = ImageTk.PhotoImage(Image.open("cap.gif"))
    captcha_img.configure(image=img)
    captcha_img.image = img
    captcha.delete(0,END)
    captcha.focus()
    
def get_captcha():
    return captcha.get()
    
def set_captcha(captcha_txt):
    captcha.insert(0, captcha_txt)
    captcha.selection_range(0, END)
    captcha.update()
    
def get_email():
    return email.get()