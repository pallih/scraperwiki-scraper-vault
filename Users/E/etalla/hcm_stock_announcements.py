import scraperwiki
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation
import urllib, urlparse
from dateutil import parser
import lxml.etree, lxml.html
import re
import json

limit = 400
offset = 0

sourcescraper = 'hcm_listed_companies'
scraperwiki.sqlite.attach(sourcescraper) 
keys =  scraperwiki.sqlite.execute('select * from `hcm_listed_companies`.swdata limit 0')['keys']
data =  scraperwiki.sqlite.select('* from `hcm_listed_companies`.swdata')


def get_announcements(symbol,name):
    announcement_feed = {}
    url = 'http://www.hsx.vn/hsx_en/Modules/Danhsach/SymbolDetail.aspx?type=S&MCty='+symbol
    root = lxml.html.parse(url).getroot()
    announcements = (root.find("body").find_class("news_symbol")[0])
    for i in announcements[1:5]: # no need to go too much back in time, as the scraper is already quite slow
        announcement_feed["title"] = i.findall("td")[0].findall("a")[0].text
        id = i.findall("td")[0].findall("a")[0].get("href")
        announcement_feed["link"]='http://www.hsx.vn/hsx_en/Modules/News/NewsDetail.aspx?id='+id[(id.find("id")+3):]
        root2 = lxml.html.parse(announcement_feed["link"]).getroot()
        announcement_feed["date"] = parser.parse(root2.find("body").find_class("news_date")[0].text.split()[0])
        announcement_feed["date"] = str(announcement_feed["date"])[:-9]
        if int(announcement_feed["date"][0:4]) > 2012:
            announcement_feed["symbol"]=symbol
            announcement_feed["company"]=name
            scraperwiki.sqlite.save(['link'],announcement_feed)


list = ["AAM","ABT","ACL","AGD","AGF","ANV","AVF","BAS","CAD","CMX","FMC","GFC","HVG","MPC","NGC","TS4","VNH","VTF","SSI","VHC"]

for i in list:
    for row in data:
        if row.get('symbol')==i:
            #print row.get('symbol')
            name = row.get('name')
            #print name
            symbol = row.get('symbol')
            get_announcements(symbol,name)