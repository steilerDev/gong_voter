from PIL import Image, ImageTk
import logging

def process_img():
    img = Image.open('cap.jpg') # Your image here!
    img = img.convert("RGBA")

    pixdata = img.load()

    # Make the letters bolder for easier recognition

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)
           
    img.save("cap.gif", "GIF")

def load_captcha_img(captcha):
    logging.info("Loading captcha: " + captcha)
    try:
        img = Image.open(captcha)
        img = img.convert("P")
    except:
        logging.error("Error loading captcha " + captcha)
        return None
    return img
    
def prepare_img_for_cintrunder(captcha, colour_id = 0):
    
    img = Image.new("P", captcha.size, 255)
    
    #Inverting picture
    temp = {}
    for x in range(captcha.size[1]):
        for y in range(captcha.size[0]):
            pix = captcha.getpixel((y, x))
            temp[pix] = pix
            if pix == colour_id: # pixel colour id 
                img.putpixel((y, x), 0)
    return img
    
def seperate_letters(image):
    inletter = False
    foundletter = False
    start = 0
    end = 0
    letters = []
            
    # Get horizontal start and end
    for y in range(image.size[0]): # slice across
        for x in range(image.size[1]): # slice down
            pix = image.getpixel((y, x))
            if pix == 255:
                inletter = True
        if foundletter == False and inletter == True:
            foundletter = True
            start = y
        if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start, end))
            logging.info("Found letter x-boundaries: (" + str(start) + " - " + str(end) + ")")
        inletter = False
    return letters
    
def extract_letters(image, letter_x_coordinates):    
    letter_images = []
    for x_coordinates in letter_x_coordinates:
        letter_image = image.crop(( x_coordinates[0], 0, x_coordinates[1], image.size[1] ))
        
        # Get vertical start and end
        inletter = False
        foundletter = False
        start = 0
        end = 0
        for x in range(letter_image.size[1]): # slice down
            for y in range(letter_image.size[0]): # slice across
                pix = letter_image.getpixel((y, x))
                if pix == 255:
                    inletter = True
            if foundletter == False and inletter == True:
                foundletter = True
                start = x
            if foundletter == True and inletter == False:
                foundletter = False
                end = x
                logging.info("Found letter y-boundaries: (" + str(start) + " - " + str(end) + ")")
                break
            inletter = False
        letter_image = image.crop((x_coordinates[0], start, x_coordinates[1], end))
        letter_images.append(letter_image)
    return letter_images