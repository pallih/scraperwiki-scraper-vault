import scraperwiki
import re
from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree
import pygooglechart
import scraperwiki.metadata
from collections import defaultdict

total = 0

def ScrapePage(page):
    global total
    url = "http://www.jrrt.org.uk/index.php?result_page=%d&page=grants-awarded&sortby=&category=" % page
    doc = lxml.html.parse(url)
    root = doc.getroot()
    trs = root.cssselect("table tr")  # skip header part
    for i in range(len(trs) / 2):
        trhead = trs[i*2 + 1]
        data = {"link":None}
        data["title"] = trhead.find("th").text
        print total, data["title"]
        trbody = trs[i*2 + 2]
        tddescription, tdamount, tdcategory, tdyear, tdawardedby = trbody.cssselect("td")

        # structures are unreliable
        description = lxml.etree.tostring(tddescription)
        pdescription = tddescription.findall("p")
        desc = re.sub("<.*?>", " ", description)
        desc = re.sub("&amp;", "&", desc)
        desc = re.sub("&#13;|&#160;", "", desc)
        desc = re.sub("\s+", " ", desc)
        data["description"] = desc.strip()
        mlink = re.search('<p class="gotowebsite">\s*<a href="(.*?)"', description)
        if mlink:
            data["link"] = mlink.group(1)
            
        amount = tdamount.text
        assert amount[0] == u'\xa3', (amount[0], '\xa3', len('\xa3'))
        data["amount"] = int(re.sub(",", "", amount[1:]))
        data["year"] = tdyear.text
        data["awardedby"] = tdawardedby.text
        
        scraperwiki.datastore.save(unique_keys=["title", "year", "description", "amount"], data=data)
        total += 1
        
def Chart():
    key = 'year'  # or supplier
    aa = scraperwiki.datastore.retrieve({key:None})
    d = defaultdict(float)
    for a in aa:
        pp = a['data'][key]
        d[pp] += float(a['data']['amount'])

    years = sorted(d.keys())
        
    data = [ int(d[key]/1000)  for key in years ]
    xmax = int(max(data))

    chart = pygooglechart.StackedHorizontalBarChart(500, 325, x_range=(0, xmax), colours=["556600"])
    chart.set_title('Awards')
    chart.set_bar_width(12)

    chart.set_axis_labels(pygooglechart.Axis.LEFT, reversed(years))
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, map(str, range(0,xmax,xmax/5)))
    chart.add_data(data)
    graph_url = chart.get_url()
    print graph_url
    scraperwiki.metadata.save("chart", graph_url)
    
    
# iterate through the pages
#for i in range(1, 21):
#    print "Page", i
#    ScrapePage(i)
Chart()


import scraperwiki
import re
from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree
import pygooglechart
import scraperwiki.metadata
from collections import defaultdict

total = 0

def ScrapePage(page):
    global total
    url = "http://www.jrrt.org.uk/index.php?result_page=%d&page=grants-awarded&sortby=&category=" % page
    doc = lxml.html.parse(url)
    root = doc.getroot()
    trs = root.cssselect("table tr")  # skip header part
    for i in range(len(trs) / 2):
        trhead = trs[i*2 + 1]
        data = {"link":None}
        data["title"] = trhead.find("th").text
        print total, data["title"]
        trbody = trs[i*2 + 2]
        tddescription, tdamount, tdcategory, tdyear, tdawardedby = trbody.cssselect("td")

        # structures are unreliable
        description = lxml.etree.tostring(tddescription)
        pdescription = tddescription.findall("p")
        desc = re.sub("<.*?>", " ", description)
        desc = re.sub("&amp;", "&", desc)
        desc = re.sub("&#13;|&#160;", "", desc)
        desc = re.sub("\s+", " ", desc)
        data["description"] = desc.strip()
        mlink = re.search('<p class="gotowebsite">\s*<a href="(.*?)"', description)
        if mlink:
            data["link"] = mlink.group(1)
            
        amount = tdamount.text
        assert amount[0] == u'\xa3', (amount[0], '\xa3', len('\xa3'))
        data["amount"] = int(re.sub(",", "", amount[1:]))
        data["year"] = tdyear.text
        data["awardedby"] = tdawardedby.text
        
        scraperwiki.datastore.save(unique_keys=["title", "year", "description", "amount"], data=data)
        total += 1
        
def Chart():
    key = 'year'  # or supplier
    aa = scraperwiki.datastore.retrieve({key:None})
    d = defaultdict(float)
    for a in aa:
        pp = a['data'][key]
        d[pp] += float(a['data']['amount'])

    years = sorted(d.keys())
        
    data = [ int(d[key]/1000)  for key in years ]
    xmax = int(max(data))

    chart = pygooglechart.StackedHorizontalBarChart(500, 325, x_range=(0, xmax), colours=["556600"])
    chart.set_title('Awards')
    chart.set_bar_width(12)

    chart.set_axis_labels(pygooglechart.Axis.LEFT, reversed(years))
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, map(str, range(0,xmax,xmax/5)))
    chart.add_data(data)
    graph_url = chart.get_url()
    print graph_url
    scraperwiki.metadata.save("chart", graph_url)
    
    
# iterate through the pages
#for i in range(1, 21):
#    print "Page", i
#    ScrapePage(i)
Chart()


import scraperwiki
import re
from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree
import pygooglechart
import scraperwiki.metadata
from collections import defaultdict

total = 0

def ScrapePage(page):
    global total
    url = "http://www.jrrt.org.uk/index.php?result_page=%d&page=grants-awarded&sortby=&category=" % page
    doc = lxml.html.parse(url)
    root = doc.getroot()
    trs = root.cssselect("table tr")  # skip header part
    for i in range(len(trs) / 2):
        trhead = trs[i*2 + 1]
        data = {"link":None}
        data["title"] = trhead.find("th").text
        print total, data["title"]
        trbody = trs[i*2 + 2]
        tddescription, tdamount, tdcategory, tdyear, tdawardedby = trbody.cssselect("td")

        # structures are unreliable
        description = lxml.etree.tostring(tddescription)
        pdescription = tddescription.findall("p")
        desc = re.sub("<.*?>", " ", description)
        desc = re.sub("&amp;", "&", desc)
        desc = re.sub("&#13;|&#160;", "", desc)
        desc = re.sub("\s+", " ", desc)
        data["description"] = desc.strip()
        mlink = re.search('<p class="gotowebsite">\s*<a href="(.*?)"', description)
        if mlink:
            data["link"] = mlink.group(1)
            
        amount = tdamount.text
        assert amount[0] == u'\xa3', (amount[0], '\xa3', len('\xa3'))
        data["amount"] = int(re.sub(",", "", amount[1:]))
        data["year"] = tdyear.text
        data["awardedby"] = tdawardedby.text
        
        scraperwiki.datastore.save(unique_keys=["title", "year", "description", "amount"], data=data)
        total += 1
        
def Chart():
    key = 'year'  # or supplier
    aa = scraperwiki.datastore.retrieve({key:None})
    d = defaultdict(float)
    for a in aa:
        pp = a['data'][key]
        d[pp] += float(a['data']['amount'])

    years = sorted(d.keys())
        
    data = [ int(d[key]/1000)  for key in years ]
    xmax = int(max(data))

    chart = pygooglechart.StackedHorizontalBarChart(500, 325, x_range=(0, xmax), colours=["556600"])
    chart.set_title('Awards')
    chart.set_bar_width(12)

    chart.set_axis_labels(pygooglechart.Axis.LEFT, reversed(years))
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, map(str, range(0,xmax,xmax/5)))
    chart.add_data(data)
    graph_url = chart.get_url()
    print graph_url
    scraperwiki.metadata.save("chart", graph_url)
    
    
# iterate through the pages
#for i in range(1, 21):
#    print "Page", i
#    ScrapePage(i)
Chart()


import scraperwiki
import re
from lxml.cssselect import CSSSelector
import lxml.html
import lxml.etree
import pygooglechart
import scraperwiki.metadata
from collections import defaultdict

total = 0

def ScrapePage(page):
    global total
    url = "http://www.jrrt.org.uk/index.php?result_page=%d&page=grants-awarded&sortby=&category=" % page
    doc = lxml.html.parse(url)
    root = doc.getroot()
    trs = root.cssselect("table tr")  # skip header part
    for i in range(len(trs) / 2):
        trhead = trs[i*2 + 1]
        data = {"link":None}
        data["title"] = trhead.find("th").text
        print total, data["title"]
        trbody = trs[i*2 + 2]
        tddescription, tdamount, tdcategory, tdyear, tdawardedby = trbody.cssselect("td")

        # structures are unreliable
        description = lxml.etree.tostring(tddescription)
        pdescription = tddescription.findall("p")
        desc = re.sub("<.*?>", " ", description)
        desc = re.sub("&amp;", "&", desc)
        desc = re.sub("&#13;|&#160;", "", desc)
        desc = re.sub("\s+", " ", desc)
        data["description"] = desc.strip()
        mlink = re.search('<p class="gotowebsite">\s*<a href="(.*?)"', description)
        if mlink:
            data["link"] = mlink.group(1)
            
        amount = tdamount.text
        assert amount[0] == u'\xa3', (amount[0], '\xa3', len('\xa3'))
        data["amount"] = int(re.sub(",", "", amount[1:]))
        data["year"] = tdyear.text
        data["awardedby"] = tdawardedby.text
        
        scraperwiki.datastore.save(unique_keys=["title", "year", "description", "amount"], data=data)
        total += 1
        
def Chart():
    key = 'year'  # or supplier
    aa = scraperwiki.datastore.retrieve({key:None})
    d = defaultdict(float)
    for a in aa:
        pp = a['data'][key]
        d[pp] += float(a['data']['amount'])

    years = sorted(d.keys())
        
    data = [ int(d[key]/1000)  for key in years ]
    xmax = int(max(data))

    chart = pygooglechart.StackedHorizontalBarChart(500, 325, x_range=(0, xmax), colours=["556600"])
    chart.set_title('Awards')
    chart.set_bar_width(12)

    chart.set_axis_labels(pygooglechart.Axis.LEFT, reversed(years))
    chart.set_axis_labels(pygooglechart.Axis.BOTTOM, map(str, range(0,xmax,xmax/5)))
    chart.add_data(data)
    graph_url = chart.get_url()
    print graph_url
    scraperwiki.metadata.save("chart", graph_url)
    
    
# iterate through the pages
#for i in range(1, 21):
#    print "Page", i
#    ScrapePage(i)
Chart()


