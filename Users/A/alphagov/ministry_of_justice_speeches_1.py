import scraperwiki
import sys
from lxml import etree
from Levenshtein import ratio

base_url = "http://www.justice.gov.uk"
start_url = base_url + "/news/speeches.htm"

ministers = []
doc = etree.HTML(scraperwiki.scrape(base_url + "/about/ministers.htm"))
for minister in doc.xpath("//div[@class='minister']//a"):
    ministers.append(minister.text)

def find_minister(text):
    best_ratio = 0
    best_minister = ''
    for m in ministers:
        r = ratio(text, m)
        if r > best_ratio:
            best_ratio = r
            best_minister = m

    return best_minister

doc = etree.HTML(scraperwiki.scrape(start_url))
for year in doc.xpath("//div[@class='minister']//a"):
    doc = etree.HTML(scraperwiki.scrape(base_url + year.attrib['href']))
    for month in doc.xpath("//div[@class='minister']//a"):
        doc = etree.HTML(scraperwiki.scrape(base_url + month.attrib['href']))
        for speech in doc.xpath("//div[contains(@class, 'news-story')]"):
            title = speech.xpath("div/h3/a")[0].text
            link = speech.xpath("div/h3/a")[0].attrib['href']
            date = speech.xpath("div/p/strong")[0].text
            
            doc = etree.HTML(scraperwiki.scrape(base_url + link))
            m = doc.xpath("//div[@id='LeftCenterRight']/img")[0].attrib['alt']
            minister = find_minister(m)

            body = '\n\n'.join([etree.tostring(p) for p in doc.xpath("//div[@id='LeftCenterRight']/p")])

            data = {
                "minister_name": minister,
                "permalink": base_url + link,
                "title": title,
                "given_on": date,
                "body": body,
                "department": "Ministry of Justice",
            }
            scraperwiki.sqlite.save(["permalink"], data)
import scraperwiki
import sys
from lxml import etree
from Levenshtein import ratio

base_url = "http://www.justice.gov.uk"
start_url = base_url + "/news/speeches.htm"

ministers = []
doc = etree.HTML(scraperwiki.scrape(base_url + "/about/ministers.htm"))
for minister in doc.xpath("//div[@class='minister']//a"):
    ministers.append(minister.text)

def find_minister(text):
    best_ratio = 0
    best_minister = ''
    for m in ministers:
        r = ratio(text, m)
        if r > best_ratio:
            best_ratio = r
            best_minister = m

    return best_minister

doc = etree.HTML(scraperwiki.scrape(start_url))
for year in doc.xpath("//div[@class='minister']//a"):
    doc = etree.HTML(scraperwiki.scrape(base_url + year.attrib['href']))
    for month in doc.xpath("//div[@class='minister']//a"):
        doc = etree.HTML(scraperwiki.scrape(base_url + month.attrib['href']))
        for speech in doc.xpath("//div[contains(@class, 'news-story')]"):
            title = speech.xpath("div/h3/a")[0].text
            link = speech.xpath("div/h3/a")[0].attrib['href']
            date = speech.xpath("div/p/strong")[0].text
            
            doc = etree.HTML(scraperwiki.scrape(base_url + link))
            m = doc.xpath("//div[@id='LeftCenterRight']/img")[0].attrib['alt']
            minister = find_minister(m)

            body = '\n\n'.join([etree.tostring(p) for p in doc.xpath("//div[@id='LeftCenterRight']/p")])

            data = {
                "minister_name": minister,
                "permalink": base_url + link,
                "title": title,
                "given_on": date,
                "body": body,
                "department": "Ministry of Justice",
            }
            scraperwiki.sqlite.save(["permalink"], data)
