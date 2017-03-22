import requests
import re
import urllib
import logging

url = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
imagelink = 'http://www.radiogong.com/index.php?eID=sr_freecap_captcha&amp;id=563'
requestlink = 'http://www.radiogong.com/radio-gong-open-air-fuer-deinen-ort/radio-gong-open-air-fuer-deinen-ort-voting.html' \
              '?tx_powermail_pi1%5BmailID%5D=26936&cHash=70044b31419eed65a274745753f82d11#c26936'
cookie = {'fe_typo_user': ''}

def reset():
    logging.info("Resetting captcha")
    html_response = requests.get(url, headers=headers)
    logging.info(pretty_print(html_response.request))
    
    global cookie
    cookie = {'fe_typo_user': html_response.cookies.values()[0]}
    img_response = requests.get(imagelink, headers=headers, cookies=cookie)
    with open("cap.jpg", "wb") as code:
        code.write(img_response.content)

def post(email, cap):
    logging.info("Posting: email = " + email + ", captcha = " + cap)
    if re.search('[a-zA-Z]', cap):
        return False

    r = requests.post(requestlink,
                      cookies=cookie,
                      files={'tx_powermail_pi1[uid36495]': (None, 'Neubrunn'), 
                             'tx_powermail_pi1[uid36497]': (None, email), 
                             'tx_powermail_pi1[uid36507]': (None, cap)},
                      headers=headers)
                      
    logging.info(pretty_print(r.request))
    
    if len(re.findall('Deine Stimme wurde erfolgreich verschickt und ist soeben bei uns angekommen(.*?)span>', r.text)) > 0:
        logging.info("Vote successful!")
        return True
    else:
        logging.error("Vote not successful!")
        return False

def pretty_print(req):
    return '{}\n{}\n{}\n\n{}'.format(
        '-----------REQUEST-START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    )