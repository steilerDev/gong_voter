import logging
from PIL import ImageTk
from Tkinter import *


class GUI:

    def __init__(self, controller):
        logging.info("Initiating GUI")

        self.window = Tk()

        self.captcha_img = Label(self.window)
        self.captcha_img.pack(side="top", fill="both", expand="yes")

        self.email = Entry(self.window)
        self.email.insert(0, "your@email.de")
        self.email.pack()

        self.captcha = Entry(self.window)
        self.captcha.bind("<Return>", controller.enter)
        self.captcha.pack()

        self.info = Label(self.window, text="0 0 0 0 0")
        self.info.pack()

        self.counter_label = Label(self.window, text="Successful votes: 0")
        self.counter_label.pack()

        self.successful_votes = 0
        logging.info("Successful initiated GUI")

    def start(self):
        self.email.focus()
        self.email.selection_range(0, END)
        self.window.mainloop()

    def send(self):
        logging.info("GUI received SEND")
        self.info.configure(text="SENT")
        self.info.update()

    def success(self):
        logging.info("GUI received SUCCESS")
        self.info.configure(text="Vote successful!")
        self.info.update()
        self.successful_votes += 1
        self.counter_label.configure(text="Successful votes: " + str(self.successful_votes))
        self.counter_label.update()

    def error(self):
        logging.error("GUI received ERROR")
        self.info.configure(text="ERROR")
        self.info.update()

    # Expects captcha to be solved
    def set_captcha(self, captcha):
        logging.info("Resetting captcha")
        self.info.configure(text="Enter CapKey")
        self.info.update()
        image = ImageTk.PhotoImage(captcha.image)
        self.captcha_img.configure(image=image)
        self.captcha_img.image = image
        self.captcha.delete(0, END)

        captcha_solution = ""
        for letter in captcha.letters:
            captcha_solution += letter.letter
        self.captcha.insert(0, captcha_solution)
        self.captcha.update()
        self.captcha.focus()
        self.captcha.selection_range(0, END)

    def get_captcha(self):
        return self.captcha.get()

    def get_email(self):
        return self.email.get()