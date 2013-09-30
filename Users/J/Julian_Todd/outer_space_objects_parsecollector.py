import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
import scraperwiki
import lxml.etree, lxml.html
import datetime
import re
import urlparse

# needs converting to using the new sqlite.save() function instead

gheaders = ['International Designator', 'Name of Space Object', 'State/ Organization', 
             'Date of Launch', 'GSO Location', 'Nuclear Power Source', 'UN Registered', 
             'Document of Registration', 'Status', 'Date of Decay or Change', 
             'Document of Decay or Change', 'Function of Space Object', 'Remarks', 'External Web Site']

osobjectfields = [ "%s text" % re.sub("[ /]", "_", h) for h in gheaders ]


fetchstep = 8

def Main():
    scraperwiki.sqlite.execute("drop table if exists osobjects")
    scraperwiki.sqlite.execute("create table osobjects (%s)" % ",".join(osobjectfields))
    scraperwiki.sqlite.attach("outer_space_objects_scrapedownloader", "src")

    for s in range(1000):
        print s
        res = scraperwiki.sqlite.execute("select html from src.osoindex order by rowid desc limit ? offset ?", (fetchstep, s*fetchstep))
        if len(res.get('data')) == 0:
            break
        for row in res.get('data'):
            ParseIndex(row[0])

def parsedate(v):
    return datetime.datetime.strptime(v, "%d/%m/%Y").date().strftime("%Y-%m-%d")

currenturl = "http://www.unoosa.org/oosa/showSearch.do"

def ParseIndex(html):
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table")
    if len(tables) < 2:
        print html
        return
    maintable = tables[1]
    rows = maintable.cssselect("tr")
    headers = [ lxml.etree.tostring(th, method="text").strip()  for th in rows[0].cssselect("th") ]

    assert headers == gheaders, headers

    for row in rows[1:]:
        columns = row.cssselect("td")
        assert len(headers) == len(columns)
        values = [ lxml.etree.tostring(td, encoding=unicode, method="text").strip()  for td in columns ]

        # extract the link
        link = columns[13].cssselect("a")
        if link:
            values[13] = urlparse.urljoin(currenturl, link[0].get("href"))

        # get rid of the square bracketing and rows of dashes
        for i in range(13):
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            values[i] = re.sub("\[([^\]]*)\]", "\\1", values[i]).strip()
            if re.match("----*$", values[i]):
                values[i] = ''
            
        data = dict(zip(headers, values))

        data['Date of Launch'] = parsedate(data['Date of Launch'])
        if data['Date of Decay or Change']:
            data['Date of Decay or Change'] = parsedate(data['Date of Decay or Change'])


        # registration document
        dlink = columns[7].cssselect("a")
        if dlink:
            data["Document link"] = urlparse.urljoin(currenturl, dlink[0].get("href"))
                        
        assert data["UN Registered"] in ['Yes', 'No'], data

        scraperwiki.sqlite.execute("insert into osobjects values (%s)" % ",".join(["?"]*len(gheaders)), 
                      tuple([data[h]  for h in gheaders]), verbose=0)

    scraperwiki.sqlite.commit()

Main()
