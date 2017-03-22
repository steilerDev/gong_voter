#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
This file is part of the cintruder project, http://cintruder.03c8.net

Copyright (c) 2012/2016 psy <epsylon@riseup.net>

cintruder is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

cintruder is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with cintruder; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from PIL import Image
from operator import itemgetter
import hashlib, time, sys, subprocess, platform
import logging
import vote_image

class CIntruderTraining(object):
    """
    Class to apply OCR techniques into captchas (general algorithm)
    """
    def __init__(self, captcha, solved_captcha):
        # initialize main CIntruder
        captcha_img = vote_image.load_captcha_for_cintrunder(captcha)
        
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

if __name__ == "__main__":
    if sys.argv[1:]:
        ocr = CIntruderOCR(sys.argv[1:])
        print ("Data correctly extracted!")
    else:
        print ("You must set a captcha for learn. Ex: inputs/test1.gif")
