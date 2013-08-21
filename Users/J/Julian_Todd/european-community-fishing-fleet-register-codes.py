import scraperwiki
import mechanize
import urllib2, urlparse
import lxml.html, lxml.etree
import re

# scraperwiki.cache(True)

# http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple
#    GetCountryLinks - Gets links to all Countries
#    GetPorts - Gets links to all ports of one country
#    GetCountryPortBoats gets all boats for one country and depagenates

fromcountrynum, fromportnum = 5, 0   # continuing scraping

def Main():
    for i, label, curl in GetCountryLinks()[fromcountrynum:]:
        print "Country[%d] %s" % (i, label),
        countryports = GetPorts(curl)
        print " nports=%d" % len(countryports)
        lfromportnum = (i == fromcountrynum and fromportnum or 0)
        for j, plab, preq in countryports[lfromportnum:]:
            print "Country[%d] Port[%d] %s" % (i, j, plab)
            request = preq

            baseurl = request.get_full_url()
            while request:
                root = lxml.html.parse(urllib2.urlopen(request)).getroot()
                print lxml.etree.tostring(root)
                records = ParseBoatTable(root)
                for data in records:
       # upd        scraperwiki.datastore.save(unique_keys=['CFR'], data=data)
                    scraperwiki.sqlite.save(unique_keys=['CFR'], data=data)
                request = GetNextPage(baseurl, root)



def ParseBoatTable(root):
    trs = root.cssselect("table.tResult tr")
    
    cnodata = root.cssselect('table.tResult_nav font.red')
    if cnodata and cnodata[0].text == "No data found":
        assert len(trs) == 1, len(trs)
        return [ ]

    headers = [ th.text.strip().replace(".", "")  for th in trs[0].cssselect('th') ]
    #print lxml.etree.tostring(root)

    assert headers == [u'', 'Country', 'CFR', 'Event Code', 'Event Date', 'Ext Marking', 'Vessel Name', 'Port Name', 'Gt Tonnage', 'LOA', 'Main Power', 'Ircs'], headers
    records = [ ]
    for tr in trs[1:]:
        vals = [ ]
        for td in tr.cssselect("td"):
            tdv = (len(td) and td[0].text or td.text).strip()
            vals.append(tdv)
        data = dict(zip(headers[1:], vals[1:]))
        records.append(data)
    return records


def GetNextPage(baseurl, root):
    # the next button
    chdebut = None
    for bn in root.cssselect("table#MyTable2 a b"):
        #print bn.text
        if bn.text == 'Next':
            ocl = bn.getparent().attrib.get('onclick')
            mocl = re.match('return changedebut\((\d+)\)', ocl)
            assert mocl, ocl
            chdebut = int(mocl.group(1))

    if not chdebut:
        return False

    print "Debut", chdebut
    nurl = None
    for js in root.cssselect("script"):
        if re.search("function changedebut", js.text or ""):
            mjurl = re.search('var url="(index.cfm?.*?)"\+valeur\+"(&download=)"\+download;', js.text)
            assert mjurl, js.text
            #print mjurl.groups()
            nurl = "%s%d%sundefined" % (mjurl.group(1), chdebut, mjurl.group(2))

    return urlparse.urljoin(baseurl, nurl)


def GetCountryLinks():
    surl = "http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(surl)
    br.select_form('SimpleSearchForm')
    citems = br.form.find_control('pays').items
    assert citems[1].name == "index.cfm?method=Search.SearchSimple&country="
    result = [ ]
    for citem in citems[2:]:
        result.append((len(result), citem.attrs.get('label'), urlparse.urljoin(surl, citem.name)))
    return result


def GetPorts(curl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(curl)
    br.select_form('SimpleSearchForm')
    pitems = br.form.find_control('ss_char_port_key').items
    assert pitems[0].name == ''
    result = [ ]
    for pitem in pitems[1:]:
        br['ss_char_port_key'] = [ pitem.name ]
        response = br.click()
        result.append((len(result), pitem.attrs.get('label'), response))
    return result

Main()


import scraperwiki
import mechanize
import urllib2, urlparse
import lxml.html, lxml.etree
import re

# scraperwiki.cache(True)

# http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple
#    GetCountryLinks - Gets links to all Countries
#    GetPorts - Gets links to all ports of one country
#    GetCountryPortBoats gets all boats for one country and depagenates

fromcountrynum, fromportnum = 5, 0   # continuing scraping

def Main():
    for i, label, curl in GetCountryLinks()[fromcountrynum:]:
        print "Country[%d] %s" % (i, label),
        countryports = GetPorts(curl)
        print " nports=%d" % len(countryports)
        lfromportnum = (i == fromcountrynum and fromportnum or 0)
        for j, plab, preq in countryports[lfromportnum:]:
            print "Country[%d] Port[%d] %s" % (i, j, plab)
            request = preq

            baseurl = request.get_full_url()
            while request:
                root = lxml.html.parse(urllib2.urlopen(request)).getroot()
                print lxml.etree.tostring(root)
                records = ParseBoatTable(root)
                for data in records:
       # upd        scraperwiki.datastore.save(unique_keys=['CFR'], data=data)
                    scraperwiki.sqlite.save(unique_keys=['CFR'], data=data)
                request = GetNextPage(baseurl, root)



def ParseBoatTable(root):
    trs = root.cssselect("table.tResult tr")
    
    cnodata = root.cssselect('table.tResult_nav font.red')
    if cnodata and cnodata[0].text == "No data found":
        assert len(trs) == 1, len(trs)
        return [ ]

    headers = [ th.text.strip().replace(".", "")  for th in trs[0].cssselect('th') ]
    #print lxml.etree.tostring(root)

    assert headers == [u'', 'Country', 'CFR', 'Event Code', 'Event Date', 'Ext Marking', 'Vessel Name', 'Port Name', 'Gt Tonnage', 'LOA', 'Main Power', 'Ircs'], headers
    records = [ ]
    for tr in trs[1:]:
        vals = [ ]
        for td in tr.cssselect("td"):
            tdv = (len(td) and td[0].text or td.text).strip()
            vals.append(tdv)
        data = dict(zip(headers[1:], vals[1:]))
        records.append(data)
    return records


def GetNextPage(baseurl, root):
    # the next button
    chdebut = None
    for bn in root.cssselect("table#MyTable2 a b"):
        #print bn.text
        if bn.text == 'Next':
            ocl = bn.getparent().attrib.get('onclick')
            mocl = re.match('return changedebut\((\d+)\)', ocl)
            assert mocl, ocl
            chdebut = int(mocl.group(1))

    if not chdebut:
        return False

    print "Debut", chdebut
    nurl = None
    for js in root.cssselect("script"):
        if re.search("function changedebut", js.text or ""):
            mjurl = re.search('var url="(index.cfm?.*?)"\+valeur\+"(&download=)"\+download;', js.text)
            assert mjurl, js.text
            #print mjurl.groups()
            nurl = "%s%d%sundefined" % (mjurl.group(1), chdebut, mjurl.group(2))

    return urlparse.urljoin(baseurl, nurl)


def GetCountryLinks():
    surl = "http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(surl)
    br.select_form('SimpleSearchForm')
    citems = br.form.find_control('pays').items
    assert citems[1].name == "index.cfm?method=Search.SearchSimple&country="
    result = [ ]
    for citem in citems[2:]:
        result.append((len(result), citem.attrs.get('label'), urlparse.urljoin(surl, citem.name)))
    return result


def GetPorts(curl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(curl)
    br.select_form('SimpleSearchForm')
    pitems = br.form.find_control('ss_char_port_key').items
    assert pitems[0].name == ''
    result = [ ]
    for pitem in pitems[1:]:
        br['ss_char_port_key'] = [ pitem.name ]
        response = br.click()
        result.append((len(result), pitem.attrs.get('label'), response))
    return result

Main()


import scraperwiki
import mechanize
import urllib2, urlparse
import lxml.html, lxml.etree
import re

# scraperwiki.cache(True)

# http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple
#    GetCountryLinks - Gets links to all Countries
#    GetPorts - Gets links to all ports of one country
#    GetCountryPortBoats gets all boats for one country and depagenates

fromcountrynum, fromportnum = 5, 0   # continuing scraping

def Main():
    for i, label, curl in GetCountryLinks()[fromcountrynum:]:
        print "Country[%d] %s" % (i, label),
        countryports = GetPorts(curl)
        print " nports=%d" % len(countryports)
        lfromportnum = (i == fromcountrynum and fromportnum or 0)
        for j, plab, preq in countryports[lfromportnum:]:
            print "Country[%d] Port[%d] %s" % (i, j, plab)
            request = preq

            baseurl = request.get_full_url()
            while request:
                root = lxml.html.parse(urllib2.urlopen(request)).getroot()
                print lxml.etree.tostring(root)
                records = ParseBoatTable(root)
                for data in records:
       # upd        scraperwiki.datastore.save(unique_keys=['CFR'], data=data)
                    scraperwiki.sqlite.save(unique_keys=['CFR'], data=data)
                request = GetNextPage(baseurl, root)



def ParseBoatTable(root):
    trs = root.cssselect("table.tResult tr")
    
    cnodata = root.cssselect('table.tResult_nav font.red')
    if cnodata and cnodata[0].text == "No data found":
        assert len(trs) == 1, len(trs)
        return [ ]

    headers = [ th.text.strip().replace(".", "")  for th in trs[0].cssselect('th') ]
    #print lxml.etree.tostring(root)

    assert headers == [u'', 'Country', 'CFR', 'Event Code', 'Event Date', 'Ext Marking', 'Vessel Name', 'Port Name', 'Gt Tonnage', 'LOA', 'Main Power', 'Ircs'], headers
    records = [ ]
    for tr in trs[1:]:
        vals = [ ]
        for td in tr.cssselect("td"):
            tdv = (len(td) and td[0].text or td.text).strip()
            vals.append(tdv)
        data = dict(zip(headers[1:], vals[1:]))
        records.append(data)
    return records


def GetNextPage(baseurl, root):
    # the next button
    chdebut = None
    for bn in root.cssselect("table#MyTable2 a b"):
        #print bn.text
        if bn.text == 'Next':
            ocl = bn.getparent().attrib.get('onclick')
            mocl = re.match('return changedebut\((\d+)\)', ocl)
            assert mocl, ocl
            chdebut = int(mocl.group(1))

    if not chdebut:
        return False

    print "Debut", chdebut
    nurl = None
    for js in root.cssselect("script"):
        if re.search("function changedebut", js.text or ""):
            mjurl = re.search('var url="(index.cfm?.*?)"\+valeur\+"(&download=)"\+download;', js.text)
            assert mjurl, js.text
            #print mjurl.groups()
            nurl = "%s%d%sundefined" % (mjurl.group(1), chdebut, mjurl.group(2))

    return urlparse.urljoin(baseurl, nurl)


def GetCountryLinks():
    surl = "http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(surl)
    br.select_form('SimpleSearchForm')
    citems = br.form.find_control('pays').items
    assert citems[1].name == "index.cfm?method=Search.SearchSimple&country="
    result = [ ]
    for citem in citems[2:]:
        result.append((len(result), citem.attrs.get('label'), urlparse.urljoin(surl, citem.name)))
    return result


def GetPorts(curl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(curl)
    br.select_form('SimpleSearchForm')
    pitems = br.form.find_control('ss_char_port_key').items
    assert pitems[0].name == ''
    result = [ ]
    for pitem in pitems[1:]:
        br['ss_char_port_key'] = [ pitem.name ]
        response = br.click()
        result.append((len(result), pitem.attrs.get('label'), response))
    return result

Main()


import scraperwiki
import mechanize
import urllib2, urlparse
import lxml.html, lxml.etree
import re

# scraperwiki.cache(True)

# http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple
#    GetCountryLinks - Gets links to all Countries
#    GetPorts - Gets links to all ports of one country
#    GetCountryPortBoats gets all boats for one country and depagenates

fromcountrynum, fromportnum = 5, 0   # continuing scraping

def Main():
    for i, label, curl in GetCountryLinks()[fromcountrynum:]:
        print "Country[%d] %s" % (i, label),
        countryports = GetPorts(curl)
        print " nports=%d" % len(countryports)
        lfromportnum = (i == fromcountrynum and fromportnum or 0)
        for j, plab, preq in countryports[lfromportnum:]:
            print "Country[%d] Port[%d] %s" % (i, j, plab)
            request = preq

            baseurl = request.get_full_url()
            while request:
                root = lxml.html.parse(urllib2.urlopen(request)).getroot()
                print lxml.etree.tostring(root)
                records = ParseBoatTable(root)
                for data in records:
       # upd        scraperwiki.datastore.save(unique_keys=['CFR'], data=data)
                    scraperwiki.sqlite.save(unique_keys=['CFR'], data=data)
                request = GetNextPage(baseurl, root)



def ParseBoatTable(root):
    trs = root.cssselect("table.tResult tr")
    
    cnodata = root.cssselect('table.tResult_nav font.red')
    if cnodata and cnodata[0].text == "No data found":
        assert len(trs) == 1, len(trs)
        return [ ]

    headers = [ th.text.strip().replace(".", "")  for th in trs[0].cssselect('th') ]
    #print lxml.etree.tostring(root)

    assert headers == [u'', 'Country', 'CFR', 'Event Code', 'Event Date', 'Ext Marking', 'Vessel Name', 'Port Name', 'Gt Tonnage', 'LOA', 'Main Power', 'Ircs'], headers
    records = [ ]
    for tr in trs[1:]:
        vals = [ ]
        for td in tr.cssselect("td"):
            tdv = (len(td) and td[0].text or td.text).strip()
            vals.append(tdv)
        data = dict(zip(headers[1:], vals[1:]))
        records.append(data)
    return records


def GetNextPage(baseurl, root):
    # the next button
    chdebut = None
    for bn in root.cssselect("table#MyTable2 a b"):
        #print bn.text
        if bn.text == 'Next':
            ocl = bn.getparent().attrib.get('onclick')
            mocl = re.match('return changedebut\((\d+)\)', ocl)
            assert mocl, ocl
            chdebut = int(mocl.group(1))

    if not chdebut:
        return False

    print "Debut", chdebut
    nurl = None
    for js in root.cssselect("script"):
        if re.search("function changedebut", js.text or ""):
            mjurl = re.search('var url="(index.cfm?.*?)"\+valeur\+"(&download=)"\+download;', js.text)
            assert mjurl, js.text
            #print mjurl.groups()
            nurl = "%s%d%sundefined" % (mjurl.group(1), chdebut, mjurl.group(2))

    return urlparse.urljoin(baseurl, nurl)


def GetCountryLinks():
    surl = "http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(surl)
    br.select_form('SimpleSearchForm')
    citems = br.form.find_control('pays').items
    assert citems[1].name == "index.cfm?method=Search.SearchSimple&country="
    result = [ ]
    for citem in citems[2:]:
        result.append((len(result), citem.attrs.get('label'), urlparse.urljoin(surl, citem.name)))
    return result


def GetPorts(curl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(curl)
    br.select_form('SimpleSearchForm')
    pitems = br.form.find_control('ss_char_port_key').items
    assert pitems[0].name == ''
    result = [ ]
    for pitem in pitems[1:]:
        br['ss_char_port_key'] = [ pitem.name ]
        response = br.click()
        result.append((len(result), pitem.attrs.get('label'), response))
    return result

Main()


import scraperwiki
import mechanize
import urllib2, urlparse
import lxml.html, lxml.etree
import re

# scraperwiki.cache(True)

# http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple
#    GetCountryLinks - Gets links to all Countries
#    GetPorts - Gets links to all ports of one country
#    GetCountryPortBoats gets all boats for one country and depagenates

fromcountrynum, fromportnum = 5, 0   # continuing scraping

def Main():
    for i, label, curl in GetCountryLinks()[fromcountrynum:]:
        print "Country[%d] %s" % (i, label),
        countryports = GetPorts(curl)
        print " nports=%d" % len(countryports)
        lfromportnum = (i == fromcountrynum and fromportnum or 0)
        for j, plab, preq in countryports[lfromportnum:]:
            print "Country[%d] Port[%d] %s" % (i, j, plab)
            request = preq

            baseurl = request.get_full_url()
            while request:
                root = lxml.html.parse(urllib2.urlopen(request)).getroot()
                print lxml.etree.tostring(root)
                records = ParseBoatTable(root)
                for data in records:
       # upd        scraperwiki.datastore.save(unique_keys=['CFR'], data=data)
                    scraperwiki.sqlite.save(unique_keys=['CFR'], data=data)
                request = GetNextPage(baseurl, root)



def ParseBoatTable(root):
    trs = root.cssselect("table.tResult tr")
    
    cnodata = root.cssselect('table.tResult_nav font.red')
    if cnodata and cnodata[0].text == "No data found":
        assert len(trs) == 1, len(trs)
        return [ ]

    headers = [ th.text.strip().replace(".", "")  for th in trs[0].cssselect('th') ]
    #print lxml.etree.tostring(root)

    assert headers == [u'', 'Country', 'CFR', 'Event Code', 'Event Date', 'Ext Marking', 'Vessel Name', 'Port Name', 'Gt Tonnage', 'LOA', 'Main Power', 'Ircs'], headers
    records = [ ]
    for tr in trs[1:]:
        vals = [ ]
        for td in tr.cssselect("td"):
            tdv = (len(td) and td[0].text or td.text).strip()
            vals.append(tdv)
        data = dict(zip(headers[1:], vals[1:]))
        records.append(data)
    return records


def GetNextPage(baseurl, root):
    # the next button
    chdebut = None
    for bn in root.cssselect("table#MyTable2 a b"):
        #print bn.text
        if bn.text == 'Next':
            ocl = bn.getparent().attrib.get('onclick')
            mocl = re.match('return changedebut\((\d+)\)', ocl)
            assert mocl, ocl
            chdebut = int(mocl.group(1))

    if not chdebut:
        return False

    print "Debut", chdebut
    nurl = None
    for js in root.cssselect("script"):
        if re.search("function changedebut", js.text or ""):
            mjurl = re.search('var url="(index.cfm?.*?)"\+valeur\+"(&download=)"\+download;', js.text)
            assert mjurl, js.text
            #print mjurl.groups()
            nurl = "%s%d%sundefined" % (mjurl.group(1), chdebut, mjurl.group(2))

    return urlparse.urljoin(baseurl, nurl)


def GetCountryLinks():
    surl = "http://ec.europa.eu/fisheries/fleet/index.cfm?method=Search.SearchSimple"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(surl)
    br.select_form('SimpleSearchForm')
    citems = br.form.find_control('pays').items
    assert citems[1].name == "index.cfm?method=Search.SearchSimple&country="
    result = [ ]
    for citem in citems[2:]:
        result.append((len(result), citem.attrs.get('label'), urlparse.urljoin(surl, citem.name)))
    return result


def GetPorts(curl):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(curl)
    br.select_form('SimpleSearchForm')
    pitems = br.form.find_control('ss_char_port_key').items
    assert pitems[0].name == ''
    result = [ ]
    for pitem in pitems[1:]:
        br['ss_char_port_key'] = [ pitem.name ]
        response = br.click()
        result.append((len(result), pitem.attrs.get('label'), response))
    return result

Main()


