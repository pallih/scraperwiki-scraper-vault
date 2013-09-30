import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
import scraperwiki
import mechanize, ClientForm
import lxml.etree, lxml.html
import datetime
import re
import urlparse

lotterygrantsurl = "http://www.lottery.culture.gov.uk/AdvancedSearch.aspx"

#scraperwiki.metadata.save('lowerdate', '1998-01-01')

# Outline:
#    ScrapeLottery(datefrom, dateto) - gets all grants within a date range
#    ParseIndex(html) - parses the list of grants shown on a single page
#    ParseSingleResult(html) - parses data from single page list for single grant
# Verification of the sums, reconciliation between index data and single page data,
# and depagination is done in ScrapeLottery.

def Main():
    for i in range(10):
        slowerdate = scraperwiki.metadata.get('lowerdate', '1993-01-01')
        lowerdate = datetime.datetime.strptime(slowerdate, "%Y-%m-%d").date()
        lowerdate1 = lowerdate + datetime.timedelta(45)
        ScrapeLottery(lowerdate, lowerdate1)
        scraperwiki.metadata.save('lowerdate', lowerdate1.strftime('%Y-%m-%d'))

    # needs also to scrape backwards from present as well as from start of time


def ScrapeLottery(datefrom, dateto):
    br = mechanize.Browser()

    response = br.open(lotterygrantsurl)
    br.select_form(name="aspnetForm")
    br["ctl00$phMainContent$dropDownAwardDate"] = ["Between"]
    br["ctl00$phMainContent$txtGrantDateFrom"] = datefrom.strftime("%d/%m/%Y")
    br["ctl00$phMainContent$txtGrantDateTo"]  = (dateto - datetime.timedelta(1)).strftime("%d/%m/%Y")  # make not inclusive


    response = br.submit()
    root = lxml.html.parse(response).getroot()
    totalgrantamount = ParsePounds(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelTotalSearchAmount')[0].text)
    countgrants = int(root.cssselect('span#ctl00_phMainContent_grantSearchResults_labelResultsCount')[0].text)

    print "Scraping between", datefrom, "and", dateto, " grants", countgrants, " amount", totalgrantamount

    grantentries = ParseIndex(root, br.geturl())
    try:
        while True:
            br.select_form(name="aspnetForm")
            response = br.submit('ctl00$phMainContent$grantSearchResults$nextPage')   # throws exception
            root = lxml.html.parse(response).getroot()
            grantentries.extend(ParseIndex(root, br.geturl()))

    except ClientForm.ControlNotFoundError:
        pass

    sumtotalgrant = sum([ grantentry['Grant amount']  for grantentry in grantentries ])
    sumcountgrant = len(grantentries)
    assert abs(sumtotalgrant - totalgrantamount) < 1, (sumtotalgrant, totalgrantamount)
    assert countgrants == sumcountgrant, (countgrants, sumcountgrant)

    # finally scrape and commit individual pages
    for grantentry in grantentries:
        for i in range(3):
            try:
                root = lxml.html.parse(grantentry['url']).getroot()
            except IOError:
                root = None
        
        # if clause to catch case when IOError generated all three times at line 67
        if root is not None:
            data = ParseSingleResult(root)

            assert data['Grant Date'] == grantentry['Grant date'], (data, grantentry)
            assert data['Grant Amount'] == grantentry['Grant amount'], (data, grantentry)
            assert data['Local Authority'] == grantentry['Local authority'], (data, grantentry)
            assert data['Distributing Body'] == grantentry['Distributing body'], (data, grantentry)
            assert data['Recipient Name'] == grantentry['Recipient'], (data, grantentry)

            data['url'] = grantentry['url']
            scraperwiki.datastore.save(unique_keys=["url"], data=data)



def ParsePounds(smoney):
    assert smoney[0] == u'\xa3', smoney
    return float(smoney[1:].replace(',', '') or "0")


def ParseIndex(root, baseurl):
    result = [ ]

    rows = root.cssselect('table.tblSearchResults tr')
    if not rows:
        return result

    headings = [ th[0].text  for th in rows[0].cssselect('th') ]

    assert headings == ['Recipient', 'Project description', u'Grant amount (\xa3)', 'Grant date', 'Local authority', 'Distributing body'], headings
    for row in rows[1:]:
        drow = [ (td.text or '').strip()  for td in row.cssselect('td') ]
        drow[0] = row[0][0].text

        data = dict(zip(headings, drow))
        data['Grant amount'] = ParsePounds(data.pop(u'Grant amount (\xa3)'))
        data['Grant date'] = datetime.datetime.strptime(data['Grant date'], "%d/%m/%Y")
        data['url'] = urlparse.urljoin(baseurl, row[0][0].attrib.get('href'))

        result.append(data)
    return result


def ParseSingleResult(root):
    headings, values = [ ], [ ]
    for tr in root.cssselect('table.tblResultData tr'):
        assert len(tr) == 2 and tr[0][0][0].tag == 'font' and tr[1][0].tag == 'span', lxml.etree.tostring(tr)
        headings.append(tr[0][0][0].text)
        values.append((tr[1][0].text or '').strip())

    assert headings == ['Distributing Body', 'Good Cause', 'Recipient Name', 'Project Name', 'Grant Date', 'Grant Amount', 'Local Authority', 'Region', 'UK Constituency'], headings

    data = dict(zip(headings, values))
    data['Grant Amount'] = ParsePounds(data['Grant Amount'])
    data['Grant Date'] = datetime.datetime.strptime(data['Grant Date'], "%d/%m/%Y")
    return data
    

Main()
