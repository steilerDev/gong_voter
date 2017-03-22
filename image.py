from PIL import Image, ImageTk

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