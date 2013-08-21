import scraperwiki
import lxml.html
import urllib, urlparse
from dateutil import parser

url = "http://www.skagerakpelagic.com/sw169.asp"

months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

news_list = []
date_list = []

def get_news():
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    news_section = (root.find("body")
    .findall("table")[1]
    .findall("tr")[0]
    .findall("td")[3]
    .findall("table")[0]
    .findall("tr")[0]
    .findall("td")[0]
    .findall("table")[0]
    .findall("tr")[1]
    .findall("td")[1])

    title_links = news_section.cssselect("a")
    date_summary = news_section.cssselect("em")
    
    news = {}
    i=0
    row = 0
    ctr = 0

    while ctr<5:
        if len(title_links[row].text_content()) !=0:
            title = title_links[row].text_content()
            link ="http://www.skagerakpelagic.com/"+ title_links[row].get("href")
            list = [title, link]
            news_list.append(list)
            ctr+=1
        row+=1

    for row in date_summary:
        year = row.text.split()[1].strip(":")
        month = months[row.text.split()[0]]
        date = "%s-%s-01" %(year,month)
        date = parser.parse(date)
        summary = lxml.html.tostring(row).split("/em>")[1]
        list = [date,summary]
        date_list.append(list)

    for row in range (0,5):
        news["title"],news["link"],news["date"], news["summary"] =news_list[row][0],news_list[row][1],date_list[row][0],date_list[row][1]
        scraperwiki.sqlite.save(['link'], news)

get_news()