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
import hashlib, os, math, time
import logging
import vote_image

def buildvector(im):
    d1 = {}
    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

def load_dictionary():
    path, dirs, files = os.walk("dictionary/").next()
    dictionary = dirs
    imageset = []
    logging.info("Loading dictionary...")
    for letter in dictionary:
        for img in os.listdir('dictionary/'+letter):
            temp = []
            temp.append(buildvector(Image.open("dictionary/%s/%s"%(letter, img))))
            imageset.append({letter:temp})
    return imageset

def crack(captcha):
    v = VectorCompare()
    
    dictionary = load_dictionary()
    
    captcha_img = vote_image.load_captcha_img(captcha)
    prep_captcha_img = vote_image.prepare_img_for_cintrunder(captcha_img)
    
    letter_x_coordinates = vote_image.seperate_letters(prep_captcha_img)
    letter_imgs = vote_image.extract_letters(prep_captcha_img, letter_x_coordinates)
    
    countid = 1
    word_sug = None
    for letter_img in letter_imgs:
        guess = []
        for image in dictionary:
            for letter, dict_letter_imgs in image.iteritems():
                if len(dict_letter_imgs) != 0:
                    guess.append(( v.relation(dict_letter_imgs[0], buildvector(letter_img)), letter))
        guess.sort(reverse=True)
        word_per = guess[0][0] * 100
        logging.info(str(countid) + ". letter: '" + str(guess[0][1]) + "' (Confidence: " + str(word_per) + "%)")

        if word_sug == None:
            word_sug = str(guess[0][1])
        else:
            word_sug = word_sug + str(guess[0][1])
        countid = countid + 1

    if word_sug is None:
        logging.warning("No match found, try to add more images to your dictionary")
    else:
        logging.info("Suggested Solution: [" + str(word_sug) + "]")
    return word_sug
    
class VectorCompare:
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            # print concordance 
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))
