from Tkinter import *
from PIL import Image, ImageTk

import requests
import re

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
                      files=dict(foo='bar'),
                      headers=headers,
                      data={'tx_powermail_pi1[uid36497]':'torben1234@gmx.de','tx_powermail_pi1[uid36495]': 'Aub','tx_powermail_pi1[uid36507]': cap})

    res.configure(text="SENT")
    res.update()

    if len(re.findall('Deine Stimme wurde erfolgreich verschickt und ist soeben bei uns angekommen(.*?)span>', r.text)) > 0:
        res.configure(text="Vote erfolgreich")
        res.update()
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



window = Tk()

#img = ImageTk.PhotoImage(Image.open("cap.jpg"))
panel = Label(window)
panel.pack(side = "top", fill = "both", expand = "yes")

entry = Entry(window)
entry.bind("<Return>", enter)
entry.pack()
res = Label(window, text="0 0 0 0 0")
res.pack()

init()
update_img()

window.mainloop()
