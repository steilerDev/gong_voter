from controller import Controller
import logging_vote

if __name__ == '__main__':
    print "Supporting Neubrunn at Radio-Gong Buergermeisterschaft 2017"
    print "Build by Lukas Bauer, adopted for Windoof & enhanced by Frank Steiler"
    print "Captcha recognition by cintruder (https://github.com/epsylon/cintruder)"
    print

    logging_vote.init()
    controller = Controller()
    controller.start()
