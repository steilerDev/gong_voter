from Tkinter import *
from PIL import Image, ImageTk

import requests
import re
import urllib

url = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
imagelink = 'http://www.radiogong.com/index.php?eID=sr_freecap_captcha&amp;id=563'
requestlink = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html' \
              '?tx_powermail_pi1%5BmailID%5D=26936&cHash=70044b31419eed65a274745753f82d11#c26936'

cookie = {'fe_typo_user': ''}

def enter(event):
    cap = entry.get()
    res.configure(text=cap)
    res.update()

    if re.search('[a-zA-Z]', cap):
        exit()

    r = requests.post(requestlink,
                      cookies=cookie,
                      files={'tx_powermail_pi1[uid36495]': (None, 'Neubrunn'), 
                             'tx_powermail_pi1[uid36497]': (None, email.get()), 
                             'tx_powermail_pi1[uid36507]': (None,cap)},
                      headers=headers)

    res.configure(text="SENT")
    res.update()

    #pretty_print_POST(r.request)
	
    if len(re.findall('Deine Stimme wurde erfolgreich verschickt und ist soeben bei uns angekommen(.*?)span>', r.text)) > 0:
        res.configure(text="Vote erfolgreich")
        res.update()
        global counter
        counter += 1
        counter_label.configure(text= "Successfull votes: " + str(counter))
        counter_label.update()
    else:
        res.configure(text="ERROR")
        res.update()

    init()
    update_img()

    entry.delete(0,END)
    entry.focus()

def init():
    html_response = requests.get(url, headers=headers)
    global cookie
    cookie = {'fe_typo_user': html_response.cookies.values()[0]}
    img_response = requests.get(imagelink, headers=headers, cookies=cookie)
    with open("cap.jpg", "wb") as code:
        code.write(img_response.content)
    res.configure(text="Enter CapKey")

def update_img():
    img2 = ImageTk.PhotoImage(Image.open("cap.jpg"))
    panel.configure(image=img2)
    panel.image = img2

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


    
print "Supporting Neubrunn at Radio-Gong Buergermeisterschaft 2017"
print "Build by Lukas Bauer, adopted for Windoof & enhanced by Frank Steiler"

window = Tk()

panel = Label(window)
panel.pack(side = "top", fill = "both", expand = "yes")

email = Entry(window)
email.insert(0,"your@email.de")
email.focus()
email.selection_range(0, END)
email.pack()

entry = Entry(window)
entry.bind("<Return>", enter)
entry.pack()
res = Label(window, text="0 0 0 0 0")
res.pack()

counter_label = Label(window, text="Successful votes: 0")
counter_label.pack()
global counter
counter = 0

init()
update_img()

window.mainloop()
