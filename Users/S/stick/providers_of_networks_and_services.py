import scraperwiki
import lxml.html
import time

# workaround of non-working sk_SK locale
# see https://bitbucket.org/ScraperWiki/scraperwiki/issue/526/python-missing-locales
def fix_month(text):
    if isinstance(text, str):
        return text.replace('Máj', 'May').replace('Jún','Jun').replace('Júl','Jul').replace('Okt','Oct')
    else:
        return text


html = scraperwiki.scrape('http://www.teleoff.gov.sk/sk/OTR/viewpublic.php?limit=2000')
html = html.replace('\x00', ' ') # fix broken html :-)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='fotky'] tr"):
    tds = tr.cssselect("td")
    if len(tds) < 23:
        continue
    try:
        start_date = int(time.mktime(time.strptime(fix_month(tds[18].text_content()), "%Y %b")))
    except:
        start_date = None
    try:
        end_date = int(time.mktime(time.strptime(fix_month(tds[19].text_content()), "%d. %b %Y")))
    except:
        end_date = None

    try:
        ico = int(tds[2].text_content())
    except:
        ico_number = None
    try:
        symbol = int(tds[21].text_content())
    except:
        symbol = None

    data = {
        'id' : int(tds[0].text_content()),
        'provider' : tds[1].text_content(),
        'ico' : ico,
        'fixed' : tds[3].text_content() == '*',
        'radio' : tds[4].text_content() == '*',
        'mobile' : tds[5].text_content() == '*',
        'satellite' : tds[6].text_content() == '*',
        'mmds' : tds[7].text_content() == '*',
        'rtv' : tds[8].text_content() == '*',
        'catv' : tds[9].text_content() == '*',
        'rozhltv' : tds[10].text_content() == '*',
        'pts' : tds[11].text_content() == '*',
        'leased' : tds[12].text_content() == '*',
        'transmission' : tds[13].text_content() == '*',
        'internet' : tds[14].text_content() == '*',
        'voip' : tds[15].text_content() == '*',
        'retransmission' : tds[16].text_content() == '*',
        'audiotex' : tds[17].text_content() == '*',
        'others' : tds[18].text_content() == '*',
        'start' : start_date,
        'end' : end_date,
        'symbol' : symbol,
        'address' : tds[22].text_content(),
        'comment' : tds[23].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data = data)
import scraperwiki
import lxml.html
import time

# workaround of non-working sk_SK locale
# see https://bitbucket.org/ScraperWiki/scraperwiki/issue/526/python-missing-locales
def fix_month(text):
    if isinstance(text, str):
        return text.replace('Máj', 'May').replace('Jún','Jun').replace('Júl','Jul').replace('Okt','Oct')
    else:
        return text


html = scraperwiki.scrape('http://www.teleoff.gov.sk/sk/OTR/viewpublic.php?limit=2000')
html = html.replace('\x00', ' ') # fix broken html :-)
root = lxml.html.fromstring(html)

for tr in root.cssselect("table[class='fotky'] tr"):
    tds = tr.cssselect("td")
    if len(tds) < 23:
        continue
    try:
        start_date = int(time.mktime(time.strptime(fix_month(tds[18].text_content()), "%Y %b")))
    except:
        start_date = None
    try:
        end_date = int(time.mktime(time.strptime(fix_month(tds[19].text_content()), "%d. %b %Y")))
    except:
        end_date = None

    try:
        ico = int(tds[2].text_content())
    except:
        ico_number = None
    try:
        symbol = int(tds[21].text_content())
    except:
        symbol = None

    data = {
        'id' : int(tds[0].text_content()),
        'provider' : tds[1].text_content(),
        'ico' : ico,
        'fixed' : tds[3].text_content() == '*',
        'radio' : tds[4].text_content() == '*',
        'mobile' : tds[5].text_content() == '*',
        'satellite' : tds[6].text_content() == '*',
        'mmds' : tds[7].text_content() == '*',
        'rtv' : tds[8].text_content() == '*',
        'catv' : tds[9].text_content() == '*',
        'rozhltv' : tds[10].text_content() == '*',
        'pts' : tds[11].text_content() == '*',
        'leased' : tds[12].text_content() == '*',
        'transmission' : tds[13].text_content() == '*',
        'internet' : tds[14].text_content() == '*',
        'voip' : tds[15].text_content() == '*',
        'retransmission' : tds[16].text_content() == '*',
        'audiotex' : tds[17].text_content() == '*',
        'others' : tds[18].text_content() == '*',
        'start' : start_date,
        'end' : end_date,
        'symbol' : symbol,
        'address' : tds[22].text_content(),
        'comment' : tds[23].text_content()
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data = data)
