#from PIL import Image
from operator import itemgetter
import hashlib
import time
import logging
import vote_image

def train(captcha, solved_captcha):
    captcha_img = vote_image.load_captcha_img(captcha)
    
    prep_captcha_img = vote_image.prepare_img_for_cintrunder(captcha_img)
    letter_x_coordinates = vote_image.seperate_letters(prep_captcha_img)
    
    if len(letter_x_coordinates) != len(solved_captcha):
        logging.error("Size of letter array does not match length of captcha!")
        return
    else:
        logging.info("Size of letter array matches length of captcha")
    
    logging.info("Saving letters to designated dictionary folder")
    letter_imgs = vote_image.extract_letters(prep_captcha_img, letter_x_coordinates)
    count = 0
    for letter_img in letter_imgs:
        m = hashlib.md5()
        m.update("%s%s"%(time.time(), count))
        letter_img.save("dictionary/" + solved_captcha[count] + "/" + m.hexdigest() + ".gif")
        count += 1
