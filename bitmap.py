import logging
from bitarray import bitarray

BITMAP_WIDTH = 32


class Bitmap:
    def __init__(self, image, confidence=0.0, letter=""):
        self.confidence = confidence
        self.letter = letter
        self.bitmap = Bitmap.image_to_bitmap(image)
        self.count = 0
        self.refresh_count()

    def refresh_count(self):
        self.count = 0
        for line in self.bitmap:
            self.count += line.count()

    def size(self):
        return len(self.bitmap)

    def __iter__(self):
        return self.bitmap.__iter__()

    def __getitem__(self, item):
        return self.bitmap.__getitem__(item)

    # Expects a single letter, already properly sliced & B/W
    @staticmethod
    def image_to_bitmap(image):

        logging.info("Building bitmap")
        logging.debug("Bitmap:")
        bitmap = []
        for y in range(image.size[1]):
            line_string = ""
            for x in range(image.size[0]):
                # Put a one where the captcha is black and a 0 where it is white
                if image.getpixel((x, y)) == 0:
                    line_string += "1"
                else:
                    line_string += "0"

            # Adding padding for fixed size width
            if len(line_string) <= BITMAP_WIDTH:
                line_string += "0" * (BITMAP_WIDTH - len(line_string))
            else:
                logging.warn("Actual bitmap width is larger than %d: %d. Loosing information!", BITMAP_WIDTH, len(line_string))
                line_string = line_string[:BITMAP_WIDTH]
            logging.debug(line_string)
            bitmap.append(bitarray(line_string))

        return bitmap

    # Compares two bitmap objects
    @staticmethod
    def compare(bm1, bm2):
        count = 0
        if bm1.size() > bm2.size():
            for idx, line in enumerate(bm2):
                count += (line & bm1[idx]).count()
        else:
            for idx, line in enumerate(bm1):
                count += (line & bm2[idx]).count()
        logging.debug("Overlap between bitmaps is %d", count)
        return count



