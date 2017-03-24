import logging, re, urllib, requests
from PIL import Image
from io import BytesIO
from bitmap import Bitmap


HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
ROOT_URL = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html'
IMAGE_URL = 'http://www.radiogong.com/index.php?eID=sr_freecap_captcha&amp;id=563'
POST_URL = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html?tx_powermail_pi1%5BmailID%5D=26936&cHash=70044b31419eed65a274745753f82d11#c26936'

VOTE = "Neubrunn"


class Captcha:
    def __init__(self):
        self.letters = []
        self.image = None
        self.cookies = {'fe_typo_user': ''}

    ## Networking Part

    def reload_captcha(self):
        logging.info("Reloading captcha")

        self.letters = []
        self.image = None

        # First get the cookie
        html_response = requests.get(ROOT_URL, headers=HEADERS)
        logging.debug("Requesting HTML for cookie: %s", Captcha.pretty_print(html_response.request))
        self.cookies = {'fe_typo_user': html_response.cookies.values()[0]}

        # Then download and set the image
        img_response= requests.get(IMAGE_URL, headers=HEADERS, cookies=self.cookies)
        logging.debug("Requesting captcha image: %s", Captcha.pretty_print(img_response.request))
        self.image = Image.open(BytesIO(img_response.content))
        self.image = self.image.convert("RGB")

        self.process_captcha()
        self.populate_letter_bitmaps()

    def send_captcha(self, email, captcha):
        logging.info("Sending captcha: Email=%s, captcha=%s, vote=%s", email, captcha, VOTE)

        if re.search('[a-zA-Z]', captcha):
            logging.error("No characters allowed in captcha solution!")
            return False

        post_response = requests.post(POST_URL,
                                      cookies=self.cookies,
                                      files={'tx_powermail_pi1[uid36495]': (None, VOTE),
                                             'tx_powermail_pi1[uid36497]': (None, email),
                                             'tx_powermail_pi1[uid36507]': (None, captcha)},
                                      headers=HEADERS)
        logging.debug("POST request: %s", Captcha.pretty_print(post_response.request))

        if len(re.findall('Deine Stimme wurde erfolgreich verschickt und ist soeben bei uns angekommen(.*?)span>', post_response.text)) > 0:
            logging.info("Vote successful!")
            return True
        else:
            logging.error("Vote not successful!")
            logging.debug("Response:")
            logging.debug(post_response.text)
            return False

    @staticmethod
    def pretty_print(request):
        return '{}\n{}\n{}\n\n{}'.format(
            '-----------REQUEST-START-----------',
            request.method + ' ' + request.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
            request.body if request.body is not None else "No body available!",
        )

    ## Image Part

    # Makes captcha black/white and single channel
    def process_captcha(self):
        # Make the letters bolder for easier recognition

        for y in range(self.image.size[1]):
            for x in range(self.image.size[0]):
                pixel = self.image.getpixel((x, y))
                if pixel[0] < 140 or pixel[1] < 140 or pixel[2] < 140:
                    self.image.putpixel((x, y), (0, 0, 0))
                    pixel = (0, 0, 0)
                if pixel[2] > 0:
                    self.image.putpixel((x, y), (255, 255, 255))

        self.image = self.image.convert("L")

    def populate_letter_bitmaps(self):
        for letter in self.seperate_letters():
            letter = self.crop_letter(letter)
            letter.save("letter.gif")
            self.letters.append(Bitmap(self.crop_letter(letter)))

        if len(self.letters) != 5:
            logging.fatal("Unable to detect all letters!")

    # Returns an array of images of seperated (not cropped) letters
    def seperate_letters(self):
        inletter = False
        foundletter = False
        start = 0
        end = 0
        letters = []

        # Get horizontal start and end
        for x in range(self.image.size[0]):  # slice across
            for y in range(self.image.size[1]):  # slice down
                pix = self.image.getpixel((x, y))
                if pix == 0:
                    inletter = True
            if foundletter is False and inletter is True:
                foundletter = True
                start = x
            if foundletter is True and inletter is False:
                foundletter = False
                end = x
                logging.info("Found letter x-boundaries: (%d - %s)", start, end)
                letters.append(self.image.crop((start, 0, end, self.image.size[1])))
            inletter = False

        return letters

    # Returns the vertically cropped image of the letter
    def crop_letter(self, letter):
        # Get vertical start and end
        inletter = False
        foundletter = False
        start = 0
        end = 0
        for y in range(letter.size[1]):  # slice down
            for x in range(letter.size[0]):  # slice across
                pix = letter.getpixel((x, y))
                if pix == 0:
                    inletter = True

            if foundletter is False and inletter is True:
                foundletter = True
                start = y
            if foundletter is True and inletter is False:
                end = y
                logging.info("Found letter y-boundaries: (" + str(start) + " - " + str(end) + ")")
                return letter.crop((0, start, letter.size[0], end))
            inletter = False
        logging.warn("Unable to find letter boundary!")
        return letter

    def __iter__(self):
        return self.letters.__iter__()


