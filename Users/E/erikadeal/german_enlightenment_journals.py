#Author: Erika Deal

# Import system modules
import scraperwiki
import urllib
import lxml.html



# Download HTML from the web
html = scraperwiki.scrape("http://www.ub.uni-bielefeld.de/diglib/aufklaerung/zeitschriften.htm")


# Set variables for data extraction
root = lxml.html.fromstring(html)

dts = root.cssselect("dl")[0].cssselect("dt")
dds = root.cssselect("dl")[0].cssselect("dd")

titles = []
cities = []
years = []

for dt in dts:
    try:
        title = dt.cssselect("b")[0].cssselect("a")[0].text
    except IndexError:
        title = "blank"
    titles.append(title)

title_index = 0

for dd in dds:
    pubData = dd.text.encode("utf-8").strip()

    try:
        if pubData[0] != "(":
            city = pubData.split(",")[-1]
            city.rstrip(")")
        else:
            city = dd.cssselect("br")[0].tail.split(",")[-1] 
    except IndexError:
        city = "blank"
    cities.append(city)
    

    try:
        year = dd.cssselect("br")[0].tail.strip(".").split()[-1]
    except IndexError:
        year = "blank"
    years.append(year)
    
    title = titles[title_index]
    title_index +=1

    data = {
        "Title": title,
        "City": city,
        "Year": year,
    }
    
    scraperwiki.sqlite.save(unique_keys=["City", "Title", "Year"], data=data)

scraperwiki.sqlite.execute("delete from swdata where Title='blank'") 
