import scraperwiki
import requests
import lxml.html
import mechanize

baseUrl= 'https://factchecking.civiclinks.it/it/fact/?tab=recent&cat='
categories =['italian_politics','politics','current','economy','entertainment','web_tech','science']
for cat in categories: 
    url=baseUrl + cat
    html = requests.get(url).text
    br = mechanize.Browser()
    br.set_handle_robots(False)
    root = lxml.html.fromstring(html)
    for el in root.cssselect("article[class= 'row-fluid fact-minicard open-data-url']"):
        print el.text_content()
#        linkList.append(el.attrib['href'])

