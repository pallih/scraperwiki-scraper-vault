import scraperwiki
import lxml.html
import itertools


url="http://www.unhabitat.org/pmss/getElectronicVersion.aspx?nr=3387&alt=1"

pdf=scraperwiki.scrape(url)
xml=scraperwiki.pdftoxml(pdf)
root=lxml.html.fromstring(xml)
pages=[root.cssselect("page[number=123]")[0],root.cssselect("page[number=124]")[0]]

def get_cities(cities):
    r=[i.text_content() for i in itertools.islice(cities,9)]
    while r:
        yield r
        r=[i.text_content() for i in itertools.islice(cities,9)]

cities=reduce(lambda x,y: x+y,[i.cssselect("text[font=32]") for i in pages])
columns=["Country","City","CPI-5","CPI-4","Productivity_Index","Quality_of_Life_Index","Infrastructure_Index","Environmental_Index","Equity_Index"]
for city in get_cities((i for i in cities)):
    data=dict(zip(columns,city))
    data["ukey"]="%s-%s"%(data["Country"],data["City"])
    scraperwiki.sqlite.save(unique_keys=["ukey"],data=data)



