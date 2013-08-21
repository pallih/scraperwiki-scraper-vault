import scraperwiki
import time
import re
import urlparse
from scraperwiki.sqlite import save

base_link = "http://www.gg.ca/honours.aspx?q=&t=6&p=&c=&pg="
base_number = 480


columns = [
    'Name', 'Province','Medal'
]

def governorscraper(html):
    for every_instance in re.finditer('<tr>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)</tr>', html, re.DOTALL|re.S):
        Name = every_instance.group(2)
        Province = every_instance.group(4)
        Medal = every_instance.group(5)
        Province = re.sub(', ', "", Province)
        Medal = re.sub('<td>', "", Medal)
        Medal = re.sub('</td>', "", Medal)
        row_data = {'Name': Name, 'Province': Province, 'Medal': Medal}
        save([],row_data)

while base_number < 2230:
    webpage = base_link + str(base_number)
    html = scraperwiki.scrape(webpage)
    governorscraper(html)
    base_number = base_number + 1
    time.sleep(10)




