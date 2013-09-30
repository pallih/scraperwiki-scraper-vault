# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
  r = requests.get('http://www.google.com/search?rlz=1Y3NDUG_enUS495SE495&client=tablet-android-asus-nexus&sourceid=chrome-mobile&ie=UTF-8&q=Site%3Aww.berghs.se%2Fstudenter++%40+#q=site:http://www.berghs.se/en/studenter+++%40&hl=en&client=tablet-android-asus-nexus&tbo=d&rlz=1Y3NDUG_enUS495SE495&ei=0PFdULniPImP4gT_vYGIBA&start=30&sa=N&bav=on.2,or.r_gc.r_pw.&fp=f63196843d7c6fd4&biw=966&bih=555').text
  dom = lxml.html.fromstring(r)
  for student in dom.cssselect('body'):
     d = {'Email': student.cssselect('Span.st')[0].text,}
     scraperwiki.sqlite.save(['Email'], d)

scrape_people()# Zarino will put code in here.

# Follow along by creating your own scraper
# -> https://scraperwiki.com/scrapers/new/python
# and typing / copying / pasting into that

import scraperwiki
import requests
import lxml.html

def scrape_people():
  r = requests.get('http://www.google.com/search?rlz=1Y3NDUG_enUS495SE495&client=tablet-android-asus-nexus&sourceid=chrome-mobile&ie=UTF-8&q=Site%3Aww.berghs.se%2Fstudenter++%40+#q=site:http://www.berghs.se/en/studenter+++%40&hl=en&client=tablet-android-asus-nexus&tbo=d&rlz=1Y3NDUG_enUS495SE495&ei=0PFdULniPImP4gT_vYGIBA&start=30&sa=N&bav=on.2,or.r_gc.r_pw.&fp=f63196843d7c6fd4&biw=966&bih=555').text
  dom = lxml.html.fromstring(r)
  for student in dom.cssselect('body'):
     d = {'Email': student.cssselect('Span.st')[0].text,}
     scraperwiki.sqlite.save(['Email'], d)

scrape_people()