import logging, os
from bitmap import Bitmap
from PIL import Image


class Dictionary:
    def __init__(self):
        self.dict = []
        self.load_dict()

    def load_dict(self, path="dict.dat"):
        logging.info("Loading dict from %s", path)
        logging.warn("Method not implemented!")

    def save_dict(self, path="dict.dat"):
        logging.warn("Method not implemented!")

    def add_entries(self, bitmaps):
        for bitmap in bitmaps:
            self.add_entry(bitmap)

    def add_entry(self, bitmap):
        self.dict.append(bitmap)
        logging.debug("Adding new entry for letter %s, dictionary has now size %i", bitmap.letter, len(self.dict))

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

