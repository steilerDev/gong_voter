import logging, os
from bitmap import Bitmap
import bitarray
import bitmap

DICT_PATH = "dict.dat"

class Dictionary:
    def __init__(self):
        self.dict = []
        self.load_dict()

    def load_dict(self):
        if os.path.isfile(DICT_PATH):
            logging.info("Loading dict from %s", DICT_PATH)
            with open(DICT_PATH, "r") as dict_file:
                for line in dict_file:
                    logging.debug("Loading entry for letter %s", line[0])
                    bitmap_string = line[2:-1]
                    entry = []
                    if len(bitmap_string) % bitmap.BITMAP_WIDTH != 0:
                        logging.warn("Bitmap string has wrong length: %d, not adding!", len(bitmap_string))
                        logging.debug("String: %s", bitmap_string)
                    else:
                        logging.debug("Entry bitmap:")
                        for bitmap_line in range(0, len(bitmap_string), bitmap.BITMAP_WIDTH):
                            start_index = bitmap_line
                            end_index = bitmap_line + bitmap.BITMAP_WIDTH
                            entry.append(bitarray.bitarray(bitmap_string[start_index:end_index]))
                            logging.debug(bitmap_string[start_index:end_index])
                    self.dict.append(Bitmap(bitmap=entry, bitmap_string=bitmap_string, letter=line[0]))
        else:
            logging.warn("No dictionary found at %s", DICT_PATH)

    def add_entries(self, bitmaps):
        for bitmap in bitmaps:
            self.add_entry(bitmap)

    def add_entry(self, bitmap):
        self.dict.append(bitmap)
        logging.debug("Adding new entry for letter %s, dictionary has now size %i", bitmap.letter, len(self.dict))
        logging.info("Saving new entry to disc...")
        with open(DICT_PATH, "a") as dict_file:
            logging.debug("Writing to file %s : %s", DICT_PATH, bitmap.bitmap_string)
            logging.debug("Length of string %d", len(bitmap.bitmap_string))
            dict_file.write(bitmap.letter + ":" + bitmap.bitmap_string + "\n")

    def match_bitmap_with_dict(self, letter_bitmap):
        best_match = None
        best_match_count = 0

        for dict_bitmap in self.dict:
            current_count = Bitmap.compare(dict_bitmap, letter_bitmap)
            if current_count > best_match_count:
                logging.debug("Found new best match! Count: %d vs. %d: %s", current_count, best_match_count, dict_bitmap.letter)
                best_match_count = current_count
                best_match = dict_bitmap

        if best_match is not None:
            letter_bitmap.letter = best_match.letter
            letter_bitmap.confidence = (best_match_count*100)/letter_bitmap.count
        else:
            logging.warn("No match found, dict is empty!")
            letter_bitmap.letter = "0"
            letter_bitmap.confidence = 0

