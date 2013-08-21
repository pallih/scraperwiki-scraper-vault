# Blank Python
from lxml.html import parse
from mechanize import Browser

br = Browser()
response = br.open('http://www.vidal.ru/poisk_preparatov/xenical.htm')
doc = parse(response).getroot()
for h2 in doc.cssselect('div.content h2'):
    print h2.text_content()

# http://www.tylerlesmann.com/tag/screen_scraping/