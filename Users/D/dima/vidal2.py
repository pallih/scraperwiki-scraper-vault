# Blank Python
import lxml.html
import urllib

url = 'http://www.vidal.ru/poisk_preparatov/xenical.htm'

root = lxml.html.parse(url).getroot()
quotes = root.xpath('//a[@class="content"]')

print quotes[0].text_content()


# http://stackoverflow.com/questions/4710307/screen-scraping-in-lxml-with-python-extract-specific-data# Blank Python
import lxml.html
import urllib

url = 'http://www.vidal.ru/poisk_preparatov/xenical.htm'

root = lxml.html.parse(url).getroot()
quotes = root.xpath('//a[@class="content"]')

print quotes[0].text_content()


# http://stackoverflow.com/questions/4710307/screen-scraping-in-lxml-with-python-extract-specific-data