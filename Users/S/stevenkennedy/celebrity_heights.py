import scraperwiki
import lxml.html
import string

# gets celebrity heights and lists in imperial and metric

base_url = "http://www.celebheights.com/s/"
url_suf = ".html"
letters = string.ascii_uppercase
names = []
heights = []

for lett in letters:
    html = scraperwiki.scrape(base_url + lett + url_suf)
    root = lxml.html.fromstring(html)
    for name in root.xpath("//a[@class='v11']/text()"):
        names.append(name)
    for height in root.xpath("//span[@class='v11']/text()"):
        heights.append(height.replace("(","").replace(")",""))

for i in range(len(names)):
    hs = heights[i].replace("ft","").replace("in","").split(" ")
    met_h = float(hs[0])*0.3048 + float(hs[1])*0.0254
    data = {'name':names[i],'height_ft':heights[i],'height_m':"{0:.2f}m".format(met_h)}
    scraperwiki.sqlite.save(unique_keys=["name"],data=data)
     

