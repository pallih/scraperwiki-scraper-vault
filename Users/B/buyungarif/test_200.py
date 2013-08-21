#import requests
import selenium
from selenium import webdriver
import scraperwiki
import lxml.html

driver = webdriver.Firefox()
html = driver.get("https://plus.google.com/communities/111761880111267488761/members")

#html = requests.get("https://plus.google.com/communities/111761880111267488761/members", verify = False)
#html = scraperwiki.scrape("https://plus.google.com/communities/111761880111267488761/members")
root = lxml.html.fromstring(html)

#for el in root.cssselect("div.upb div.'PRb D3b'"):
#    data = {'url_id' : el.get('data-oid')}
#    print data
    #scraperwiki.sqlite.save(unique_keys = ['url_id'], data = data)
print root