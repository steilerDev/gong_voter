from dictionary import Dictionary
import logging

CONFIDENCE_THRESHOLD = 95.0


class Solver:
    def __init__(self):
        self.dict = Dictionary()

    # Returns true, if solution has high confidence to be correct
    def solve_captcha(self, captcha):
        logging.info("Trying to solve captcha...")

        high_confidence = True
        for idx, letter in enumerate(captcha):
            self.dict.match_bitmap_with_dict(letter)
            logging.info("Matched %d letter: %s (Confidence: %d %%)", idx, letter.letter, letter.confidence)
            high_confidence &= (letter.confidence > CONFIDENCE_THRESHOLD)
        return high_confidence

    def train(self, captcha, captcha_solution):
        logging.info("Learning captcha (solution: %s)", captcha_solution)
        for idx, letter in enumerate(captcha):
            if letter.letter == captcha_solution[idx]:
                if letter.confidence < CONFIDENCE_THRESHOLD:
                    logging.info("Correct prediction with low confidence -> Adding new entry for letter %s", letter.letter)
                    self.dict.add_entry(letter)
                else:
                    logging.info("Correct prediction with high confidence -> Not adding new entry for letter %s", letter.letter)
            else:
                letter.letter = captcha_solution[idx]
                logging.info("Wrong prediction -> Adding new entry for letter %s", letter.letter)
                self.dict.add_entry(letter)
