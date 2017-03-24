import logging
import logging_vote
from solver import Solver
from captcha import Captcha
from gui import GUI


class Controller:
    def __init__(self):
        logging.info("Initiating voter")
        self.solver = Solver()
        self.captcha = Captcha()
        self.gui = GUI(self)

    def start(self):
        self.reset()
        self.gui.start()

    def enter(self, event):
        self.gui.send()
        if self.captcha.send_captcha(self.gui.get_email(), self.gui.get_captcha()):
            logging.info("Successful send vote!")
            self.solver.train(self.captcha, self.gui.get_captcha())
            self.gui.success()
        else:
            logging.info("Error sending vote!")
            self.gui.error()

        self.reset()

    def reset(self):
        logging.info("Resetting voter")
        self.captcha.reload_captcha()

        if self.solver.solve_captcha(self.captcha):
            logging.info("Solved captcha with high confidence!")

        self.gui.set_captcha(self.captcha)
