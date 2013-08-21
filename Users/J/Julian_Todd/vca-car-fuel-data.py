import mechanize
import lxml.etree
import lxml.html
import re
from scraperwiki.sqlite import save

# change since first scraper: g km became mg km
expectedheadings = ['CO', 'CO Emissions g km', 'Description', 'Engine Capacity', 'Euro Standard', 'Fuel Cost 12000 miles', 
                    'Fuel Type', 'HC Emissions g km', 'HC NOx Emissions g km', 'Imperial Combined', 'Imperial Extra Urban', 
                    'Imperial Urban cold', 'Metric Combined', 'Metric Extra Urban', 'Metric Urban cold', 'Model', 
                    'NOx Emissions g km', 'Noise Level', 'Particulates No', 'Transmission']

floatvalheadings = ['Metric Combined', 'Noise Level', 'Metric Urban cold', 'CO Emissions g km', 'NOx Emissions g km', 
                    'Metric Extra Urban', 'Imperial Urban cold', 'NOx Emissions g km', 'Metric Extra Urban', 
                    'Imperial Combined', 'Imperial Urban cold', 'Particulates No', 'HC NOx Emissions g km', 'HC Emissions g km' ]



def ParseCarPage(href, make):
    pageid = re.match("vehicleDetails.asp\?id=(\d+)$", href).group(1)
    url = "http://www.vcacarfueldata.org.uk/search/" + href
    root = lxml.html.parse(url).getroot()

    headings = [ ]
    for h in root.cssselect("td.vehicleDetailsHeading strong"):
        lh = re.sub("[^a-zA-Z0-9]+", " ", h.text)
        lh = re.sub("\s+", " ", lh).strip()
        headings.append(lh)
    values = [ ]
    for v in root.cssselect("td.tableAlt3"):
        lv = (v.text or "").strip()
        if lv == "N/A":
            lv = None
        values.append(lv)

    del values[2]
    del values[-1]
    assert len(headings) == 20
    assert len(values) == len(headings)

    # normalize out the mg values to g values
    data = dict(zip(headings, values))
    for key in data.keys():
        if key[-6:] == " mg km":
            nkey = key[:-6]+" g km"
            v = data.pop(key)
            if v == None:
                data[nkey] = None
            else:
                data[nkey] = float(v)/1000

    for key in data.keys():
        if key[:4] == "THC ":
            data[key[1:]] = data.pop(key)

    for key in floatvalheadings:
        if data[key] != None:
            data[key] = float(data[key])

    assert data['Fuel Cost 12000 miles'][0] == u'\xa3'
    data['Fuel Cost 12000 miles'] = int(re.sub(",", "", data['Fuel Cost 12000 miles'][1:]))

    nheadings = sorted(data.keys())
    print nheadings
    assert nheadings == expectedheadings, [ a  for a in zip(nheadings, expectedheadings)  if a[0]!=a[1] ]

    fvalues = [ ]
    data["url"] = url
    data["make"] = make
    data["pageid"] = pageid

    print data
    return
    
    labimg = [img.attrib.get("src") for img in root.cssselect("img")  if img.attrib.get("alt") == "Fuel Consumption Label"]
    labelletter = re.match('/images/labels/label([A-Z]).gif$', labimg[0]).group(1)
    #<img src="/images/labels/labelG.gif" alt="Fuel Consumption Label"
    data["labelletter"] = labelletter    
    
    save(unique_keys=["pageid"], data=data)
    
    
def ParseIndexPage(html, page):
    root = lxml.html.fromstring(html)
    print root.cssselect("div.sectionTitle")[0].text
    t6 = root.cssselect("table")[6]
    for tr in t6.cssselect("tr")[1:]:
        td0 = tr.cssselect("td")[0]
        if td0.attrib.get("class") == "tableAlt1SearchTable":
            make = td0[0].text
            print "Make:", make
        elif "colspan" not in td0.attrib:
            href = tr.cssselect("td a")[0].attrib["href"]
            ParseCarPage(href, make)
            

def Main():                   
    url = "http://www.vcacarfueldata.org.uk/search/searchResults.asp"
    br = mechanize.Browser()
    html = br.open(url).read()
    #ParseIndexPage(html, 1)
    
    root = lxml.html.fromstring(html)
    totalpages = root.cssselect("div.sectionTitle")[0].text
    mtotalpages = re.match("Search Results - Page (\d+) of (\d+)$", totalpages)
    p1, plast = int(mtotalpages.group(1)), int(mtotalpages.group(2))
    print p1, plast
    #assert p1 == 1
    #assert 500 < plast < 600
    #p1 = 484
    for page in range(p1, plast+1):
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
        br["page"] = str(page)
        html = br.submit().read()
        ParseIndexPage(html, page)
        br.back()

print "hii"

Main()import mechanize
import lxml.etree
import lxml.html
import re
from scraperwiki.sqlite import save

# change since first scraper: g km became mg km
expectedheadings = ['CO', 'CO Emissions g km', 'Description', 'Engine Capacity', 'Euro Standard', 'Fuel Cost 12000 miles', 
                    'Fuel Type', 'HC Emissions g km', 'HC NOx Emissions g km', 'Imperial Combined', 'Imperial Extra Urban', 
                    'Imperial Urban cold', 'Metric Combined', 'Metric Extra Urban', 'Metric Urban cold', 'Model', 
                    'NOx Emissions g km', 'Noise Level', 'Particulates No', 'Transmission']

floatvalheadings = ['Metric Combined', 'Noise Level', 'Metric Urban cold', 'CO Emissions g km', 'NOx Emissions g km', 
                    'Metric Extra Urban', 'Imperial Urban cold', 'NOx Emissions g km', 'Metric Extra Urban', 
                    'Imperial Combined', 'Imperial Urban cold', 'Particulates No', 'HC NOx Emissions g km', 'HC Emissions g km' ]



def ParseCarPage(href, make):
    pageid = re.match("vehicleDetails.asp\?id=(\d+)$", href).group(1)
    url = "http://www.vcacarfueldata.org.uk/search/" + href
    root = lxml.html.parse(url).getroot()

    headings = [ ]
    for h in root.cssselect("td.vehicleDetailsHeading strong"):
        lh = re.sub("[^a-zA-Z0-9]+", " ", h.text)
        lh = re.sub("\s+", " ", lh).strip()
        headings.append(lh)
    values = [ ]
    for v in root.cssselect("td.tableAlt3"):
        lv = (v.text or "").strip()
        if lv == "N/A":
            lv = None
        values.append(lv)

    del values[2]
    del values[-1]
    assert len(headings) == 20
    assert len(values) == len(headings)

    # normalize out the mg values to g values
    data = dict(zip(headings, values))
    for key in data.keys():
        if key[-6:] == " mg km":
            nkey = key[:-6]+" g km"
            v = data.pop(key)
            if v == None:
                data[nkey] = None
            else:
                data[nkey] = float(v)/1000

    for key in data.keys():
        if key[:4] == "THC ":
            data[key[1:]] = data.pop(key)

    for key in floatvalheadings:
        if data[key] != None:
            data[key] = float(data[key])

    assert data['Fuel Cost 12000 miles'][0] == u'\xa3'
    data['Fuel Cost 12000 miles'] = int(re.sub(",", "", data['Fuel Cost 12000 miles'][1:]))

    nheadings = sorted(data.keys())
    print nheadings
    assert nheadings == expectedheadings, [ a  for a in zip(nheadings, expectedheadings)  if a[0]!=a[1] ]

    fvalues = [ ]
    data["url"] = url
    data["make"] = make
    data["pageid"] = pageid

    print data
    return
    
    labimg = [img.attrib.get("src") for img in root.cssselect("img")  if img.attrib.get("alt") == "Fuel Consumption Label"]
    labelletter = re.match('/images/labels/label([A-Z]).gif$', labimg[0]).group(1)
    #<img src="/images/labels/labelG.gif" alt="Fuel Consumption Label"
    data["labelletter"] = labelletter    
    
    save(unique_keys=["pageid"], data=data)
    
    
def ParseIndexPage(html, page):
    root = lxml.html.fromstring(html)
    print root.cssselect("div.sectionTitle")[0].text
    t6 = root.cssselect("table")[6]
    for tr in t6.cssselect("tr")[1:]:
        td0 = tr.cssselect("td")[0]
        if td0.attrib.get("class") == "tableAlt1SearchTable":
            make = td0[0].text
            print "Make:", make
        elif "colspan" not in td0.attrib:
            href = tr.cssselect("td a")[0].attrib["href"]
            ParseCarPage(href, make)
            

def Main():                   
    url = "http://www.vcacarfueldata.org.uk/search/searchResults.asp"
    br = mechanize.Browser()
    html = br.open(url).read()
    #ParseIndexPage(html, 1)
    
    root = lxml.html.fromstring(html)
    totalpages = root.cssselect("div.sectionTitle")[0].text
    mtotalpages = re.match("Search Results - Page (\d+) of (\d+)$", totalpages)
    p1, plast = int(mtotalpages.group(1)), int(mtotalpages.group(2))
    print p1, plast
    #assert p1 == 1
    #assert 500 < plast < 600
    #p1 = 484
    for page in range(p1, plast+1):
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
        br["page"] = str(page)
        html = br.submit().read()
        ParseIndexPage(html, page)
        br.back()

print "hii"

Main()import mechanize
import lxml.etree
import lxml.html
import re
from scraperwiki.sqlite import save

# change since first scraper: g km became mg km
expectedheadings = ['CO', 'CO Emissions g km', 'Description', 'Engine Capacity', 'Euro Standard', 'Fuel Cost 12000 miles', 
                    'Fuel Type', 'HC Emissions g km', 'HC NOx Emissions g km', 'Imperial Combined', 'Imperial Extra Urban', 
                    'Imperial Urban cold', 'Metric Combined', 'Metric Extra Urban', 'Metric Urban cold', 'Model', 
                    'NOx Emissions g km', 'Noise Level', 'Particulates No', 'Transmission']

floatvalheadings = ['Metric Combined', 'Noise Level', 'Metric Urban cold', 'CO Emissions g km', 'NOx Emissions g km', 
                    'Metric Extra Urban', 'Imperial Urban cold', 'NOx Emissions g km', 'Metric Extra Urban', 
                    'Imperial Combined', 'Imperial Urban cold', 'Particulates No', 'HC NOx Emissions g km', 'HC Emissions g km' ]



def ParseCarPage(href, make):
    pageid = re.match("vehicleDetails.asp\?id=(\d+)$", href).group(1)
    url = "http://www.vcacarfueldata.org.uk/search/" + href
    root = lxml.html.parse(url).getroot()

    headings = [ ]
    for h in root.cssselect("td.vehicleDetailsHeading strong"):
        lh = re.sub("[^a-zA-Z0-9]+", " ", h.text)
        lh = re.sub("\s+", " ", lh).strip()
        headings.append(lh)
    values = [ ]
    for v in root.cssselect("td.tableAlt3"):
        lv = (v.text or "").strip()
        if lv == "N/A":
            lv = None
        values.append(lv)

    del values[2]
    del values[-1]
    assert len(headings) == 20
    assert len(values) == len(headings)

    # normalize out the mg values to g values
    data = dict(zip(headings, values))
    for key in data.keys():
        if key[-6:] == " mg km":
            nkey = key[:-6]+" g km"
            v = data.pop(key)
            if v == None:
                data[nkey] = None
            else:
                data[nkey] = float(v)/1000

    for key in data.keys():
        if key[:4] == "THC ":
            data[key[1:]] = data.pop(key)

    for key in floatvalheadings:
        if data[key] != None:
            data[key] = float(data[key])

    assert data['Fuel Cost 12000 miles'][0] == u'\xa3'
    data['Fuel Cost 12000 miles'] = int(re.sub(",", "", data['Fuel Cost 12000 miles'][1:]))

    nheadings = sorted(data.keys())
    print nheadings
    assert nheadings == expectedheadings, [ a  for a in zip(nheadings, expectedheadings)  if a[0]!=a[1] ]

    fvalues = [ ]
    data["url"] = url
    data["make"] = make
    data["pageid"] = pageid

    print data
    return
    
    labimg = [img.attrib.get("src") for img in root.cssselect("img")  if img.attrib.get("alt") == "Fuel Consumption Label"]
    labelletter = re.match('/images/labels/label([A-Z]).gif$', labimg[0]).group(1)
    #<img src="/images/labels/labelG.gif" alt="Fuel Consumption Label"
    data["labelletter"] = labelletter    
    
    save(unique_keys=["pageid"], data=data)
    
    
def ParseIndexPage(html, page):
    root = lxml.html.fromstring(html)
    print root.cssselect("div.sectionTitle")[0].text
    t6 = root.cssselect("table")[6]
    for tr in t6.cssselect("tr")[1:]:
        td0 = tr.cssselect("td")[0]
        if td0.attrib.get("class") == "tableAlt1SearchTable":
            make = td0[0].text
            print "Make:", make
        elif "colspan" not in td0.attrib:
            href = tr.cssselect("td a")[0].attrib["href"]
            ParseCarPage(href, make)
            

def Main():                   
    url = "http://www.vcacarfueldata.org.uk/search/searchResults.asp"
    br = mechanize.Browser()
    html = br.open(url).read()
    #ParseIndexPage(html, 1)
    
    root = lxml.html.fromstring(html)
    totalpages = root.cssselect("div.sectionTitle")[0].text
    mtotalpages = re.match("Search Results - Page (\d+) of (\d+)$", totalpages)
    p1, plast = int(mtotalpages.group(1)), int(mtotalpages.group(2))
    print p1, plast
    #assert p1 == 1
    #assert 500 < plast < 600
    #p1 = 484
    for page in range(p1, plast+1):
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
        br["page"] = str(page)
        html = br.submit().read()
        ParseIndexPage(html, page)
        br.back()

print "hii"

Main()import mechanize
import lxml.etree
import lxml.html
import re
from scraperwiki.sqlite import save

# change since first scraper: g km became mg km
expectedheadings = ['CO', 'CO Emissions g km', 'Description', 'Engine Capacity', 'Euro Standard', 'Fuel Cost 12000 miles', 
                    'Fuel Type', 'HC Emissions g km', 'HC NOx Emissions g km', 'Imperial Combined', 'Imperial Extra Urban', 
                    'Imperial Urban cold', 'Metric Combined', 'Metric Extra Urban', 'Metric Urban cold', 'Model', 
                    'NOx Emissions g km', 'Noise Level', 'Particulates No', 'Transmission']

floatvalheadings = ['Metric Combined', 'Noise Level', 'Metric Urban cold', 'CO Emissions g km', 'NOx Emissions g km', 
                    'Metric Extra Urban', 'Imperial Urban cold', 'NOx Emissions g km', 'Metric Extra Urban', 
                    'Imperial Combined', 'Imperial Urban cold', 'Particulates No', 'HC NOx Emissions g km', 'HC Emissions g km' ]



def ParseCarPage(href, make):
    pageid = re.match("vehicleDetails.asp\?id=(\d+)$", href).group(1)
    url = "http://www.vcacarfueldata.org.uk/search/" + href
    root = lxml.html.parse(url).getroot()

    headings = [ ]
    for h in root.cssselect("td.vehicleDetailsHeading strong"):
        lh = re.sub("[^a-zA-Z0-9]+", " ", h.text)
        lh = re.sub("\s+", " ", lh).strip()
        headings.append(lh)
    values = [ ]
    for v in root.cssselect("td.tableAlt3"):
        lv = (v.text or "").strip()
        if lv == "N/A":
            lv = None
        values.append(lv)

    del values[2]
    del values[-1]
    assert len(headings) == 20
    assert len(values) == len(headings)

    # normalize out the mg values to g values
    data = dict(zip(headings, values))
    for key in data.keys():
        if key[-6:] == " mg km":
            nkey = key[:-6]+" g km"
            v = data.pop(key)
            if v == None:
                data[nkey] = None
            else:
                data[nkey] = float(v)/1000

    for key in data.keys():
        if key[:4] == "THC ":
            data[key[1:]] = data.pop(key)

    for key in floatvalheadings:
        if data[key] != None:
            data[key] = float(data[key])

    assert data['Fuel Cost 12000 miles'][0] == u'\xa3'
    data['Fuel Cost 12000 miles'] = int(re.sub(",", "", data['Fuel Cost 12000 miles'][1:]))

    nheadings = sorted(data.keys())
    print nheadings
    assert nheadings == expectedheadings, [ a  for a in zip(nheadings, expectedheadings)  if a[0]!=a[1] ]

    fvalues = [ ]
    data["url"] = url
    data["make"] = make
    data["pageid"] = pageid

    print data
    return
    
    labimg = [img.attrib.get("src") for img in root.cssselect("img")  if img.attrib.get("alt") == "Fuel Consumption Label"]
    labelletter = re.match('/images/labels/label([A-Z]).gif$', labimg[0]).group(1)
    #<img src="/images/labels/labelG.gif" alt="Fuel Consumption Label"
    data["labelletter"] = labelletter    
    
    save(unique_keys=["pageid"], data=data)
    
    
def ParseIndexPage(html, page):
    root = lxml.html.fromstring(html)
    print root.cssselect("div.sectionTitle")[0].text
    t6 = root.cssselect("table")[6]
    for tr in t6.cssselect("tr")[1:]:
        td0 = tr.cssselect("td")[0]
        if td0.attrib.get("class") == "tableAlt1SearchTable":
            make = td0[0].text
            print "Make:", make
        elif "colspan" not in td0.attrib:
            href = tr.cssselect("td a")[0].attrib["href"]
            ParseCarPage(href, make)
            

def Main():                   
    url = "http://www.vcacarfueldata.org.uk/search/searchResults.asp"
    br = mechanize.Browser()
    html = br.open(url).read()
    #ParseIndexPage(html, 1)
    
    root = lxml.html.fromstring(html)
    totalpages = root.cssselect("div.sectionTitle")[0].text
    mtotalpages = re.match("Search Results - Page (\d+) of (\d+)$", totalpages)
    p1, plast = int(mtotalpages.group(1)), int(mtotalpages.group(2))
    print p1, plast
    #assert p1 == 1
    #assert 500 < plast < 600
    #p1 = 484
    for page in range(p1, plast+1):
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
        br["page"] = str(page)
        html = br.submit().read()
        ParseIndexPage(html, page)
        br.back()

print "hii"

Main()import mechanize
import lxml.etree
import lxml.html
import re
from scraperwiki.sqlite import save

# change since first scraper: g km became mg km
expectedheadings = ['CO', 'CO Emissions g km', 'Description', 'Engine Capacity', 'Euro Standard', 'Fuel Cost 12000 miles', 
                    'Fuel Type', 'HC Emissions g km', 'HC NOx Emissions g km', 'Imperial Combined', 'Imperial Extra Urban', 
                    'Imperial Urban cold', 'Metric Combined', 'Metric Extra Urban', 'Metric Urban cold', 'Model', 
                    'NOx Emissions g km', 'Noise Level', 'Particulates No', 'Transmission']

floatvalheadings = ['Metric Combined', 'Noise Level', 'Metric Urban cold', 'CO Emissions g km', 'NOx Emissions g km', 
                    'Metric Extra Urban', 'Imperial Urban cold', 'NOx Emissions g km', 'Metric Extra Urban', 
                    'Imperial Combined', 'Imperial Urban cold', 'Particulates No', 'HC NOx Emissions g km', 'HC Emissions g km' ]



def ParseCarPage(href, make):
    pageid = re.match("vehicleDetails.asp\?id=(\d+)$", href).group(1)
    url = "http://www.vcacarfueldata.org.uk/search/" + href
    root = lxml.html.parse(url).getroot()

    headings = [ ]
    for h in root.cssselect("td.vehicleDetailsHeading strong"):
        lh = re.sub("[^a-zA-Z0-9]+", " ", h.text)
        lh = re.sub("\s+", " ", lh).strip()
        headings.append(lh)
    values = [ ]
    for v in root.cssselect("td.tableAlt3"):
        lv = (v.text or "").strip()
        if lv == "N/A":
            lv = None
        values.append(lv)

    del values[2]
    del values[-1]
    assert len(headings) == 20
    assert len(values) == len(headings)

    # normalize out the mg values to g values
    data = dict(zip(headings, values))
    for key in data.keys():
        if key[-6:] == " mg km":
            nkey = key[:-6]+" g km"
            v = data.pop(key)
            if v == None:
                data[nkey] = None
            else:
                data[nkey] = float(v)/1000

    for key in data.keys():
        if key[:4] == "THC ":
            data[key[1:]] = data.pop(key)

    for key in floatvalheadings:
        if data[key] != None:
            data[key] = float(data[key])

    assert data['Fuel Cost 12000 miles'][0] == u'\xa3'
    data['Fuel Cost 12000 miles'] = int(re.sub(",", "", data['Fuel Cost 12000 miles'][1:]))

    nheadings = sorted(data.keys())
    print nheadings
    assert nheadings == expectedheadings, [ a  for a in zip(nheadings, expectedheadings)  if a[0]!=a[1] ]

    fvalues = [ ]
    data["url"] = url
    data["make"] = make
    data["pageid"] = pageid

    print data
    return
    
    labimg = [img.attrib.get("src") for img in root.cssselect("img")  if img.attrib.get("alt") == "Fuel Consumption Label"]
    labelletter = re.match('/images/labels/label([A-Z]).gif$', labimg[0]).group(1)
    #<img src="/images/labels/labelG.gif" alt="Fuel Consumption Label"
    data["labelletter"] = labelletter    
    
    save(unique_keys=["pageid"], data=data)
    
    
def ParseIndexPage(html, page):
    root = lxml.html.fromstring(html)
    print root.cssselect("div.sectionTitle")[0].text
    t6 = root.cssselect("table")[6]
    for tr in t6.cssselect("tr")[1:]:
        td0 = tr.cssselect("td")[0]
        if td0.attrib.get("class") == "tableAlt1SearchTable":
            make = td0[0].text
            print "Make:", make
        elif "colspan" not in td0.attrib:
            href = tr.cssselect("td a")[0].attrib["href"]
            ParseCarPage(href, make)
            

def Main():                   
    url = "http://www.vcacarfueldata.org.uk/search/searchResults.asp"
    br = mechanize.Browser()
    html = br.open(url).read()
    #ParseIndexPage(html, 1)
    
    root = lxml.html.fromstring(html)
    totalpages = root.cssselect("div.sectionTitle")[0].text
    mtotalpages = re.match("Search Results - Page (\d+) of (\d+)$", totalpages)
    p1, plast = int(mtotalpages.group(1)), int(mtotalpages.group(2))
    print p1, plast
    #assert p1 == 1
    #assert 500 < plast < 600
    #p1 = 484
    for page in range(p1, plast+1):
        br.form = list(br.forms())[0]
        br.form.set_all_readonly(False)
        br["page"] = str(page)
        html = br.submit().read()
        ParseIndexPage(html, page)
        br.back()

print "hii"

Main()