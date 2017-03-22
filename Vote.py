import logging

from training import CIntruderTraining
from crack import CIntruderCrack
import gui
import vote_image
import networking
import vote_logging


def enter(event):
    gui.send()
    if networking.post(gui.get_email(), gui.get_captcha()):
        gui.success()
        trainer = CIntruderTraining("cap.gif", gui.get_captcha())
    else:
        gui.error()
        
    trainer = CIntruderTraining("cap.gif", gui.get_captcha())
    reset()

def reset():
    logging.info("Resetting...")
    #networking.reset()
    vote_image.process_img()
    gui.reset()
    try_crack()
    
def try_crack():
    cracker = CIntruderCrack("cap.gif")
    result = cracker.crack()
    if result is not None and len(result) == 5:
        logging.info("Cracker produced: " + result)
        gui.set_captcha(result)
    else:
        logging.warning("Cracker produced no result")

if __name__ == '__main__':
    print "Supporting Neubrunn at Radio-Gong Buergermeisterschaft 2017"
    print "Build by Lukas Bauer, adopted for Windoof & enhanced by Frank Steiler"
    print "Captcha recognition by cintruder (https://github.com/epsylon/cintruder)"
    print

    vote_logging.init(level=logging.DEBUG)
    gui.init()
    reset()
    gui.start()

