# -*- coding: utf-8 -*-

"""
    Aggregator for precipitation data from Hesse/Germany

    Source: Hessisches Landesamt für Umwelt und Geologie
"""

# http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html

import scraperwiki
import mechanize
import re, sys, random
from BeautifulSoup import BeautifulSoup
import scrapemark
import xlrd
import urllib2 as urllib

def shuffle(l):
    """Sort a list in random order"""
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def get_stations():
    """Get meta data about the precipitation sensor stations"""
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html")
    assert br.viewing_html()
    response = br.response()
    soup = BeautifulSoup(response.read())
    tables = soup.findAll('table', attrs={'class': 'contenttable'})
    for table in tables:
        headcolumns = table.findAll('th')
        if len(headcolumns) == 9:
            # correct number of columns - this means we have the right table.
            tbody = table.findAll('tbody')[0]
            rows = []
            # Name, Kurzname, HLUG Messstellennummer, Rechtswert, Hochwert, Geländehöhe, Tagesmessungen seit, Geräte, Betreiber* der Geräte
            fieldnames = ['name', 'shortname', 'id', 'coord_right', 'coord_top', 'altitude', 'since', None, 'operator']
            for tr in tbody.findAll('tr'):
                tds = tr.findAll('td')
                row = {}
                for n in range(0, len(tds)):
                    if fieldnames[n] is not None and tds[n] is not None and tds[n].contents[0] is not None:
                        try:
                            content = str(tds[n].contents[0])
                            content = re.sub(r'<[/]{0,1}[^>]+>', '', content) # remove extra tags
                            content = content.strip()
                            if content != "keine":
                                row[fieldnames[n]] = content
                        except:
                            print "Could not strip field", n, fieldnames[n], tds[n]
                rows.append(row)
                #print row
            #print rows
            scraperwiki.sqlite.save(unique_keys=['id'], data=rows, table_name="stations")

def get_values():
    """Get actual readings from the stations"""
    baseurl = 'http://www.hlug.de/static/pegel/static/'
    listpageurl = baseurl + "list_N_0.htm?entryparakey=N"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(listpageurl)
    assert br.viewing_html()
    links = []
    for link in br.links(url_regex=".*stat_[0-9]+.htm\?entryparakey=N"):
        links.append(link.url)
    links = shuffle(links)
    for link in links:
        subpageurl = baseurl + link
        print "Fetching", subpageurl
        br.open(subpageurl)
        html = br.response().read()
        station = scrapemark.scrape("""
                <table class="wwp_sdheader" cellpadding=4 width=720>
                    <tr>
                        <td class="wwp_sdheader" colspan=6>Station</td>
                    </tr>
                    <tr>
                        <td class="head">Name</td><td class="td1">{{ name }}</td>
                        <td class="head">Messstellen-Nr.</td><td class="td1">{{ id|int }}</td>
                        <td class="head">Flussgebiet</td><td class="td1">{{ river }}</td>
                    </tr>
                </table>
                <a target="_blank" class="graphlink" href="data_{{ linkid }}_N_WEEK.xls">4-Tage</a>
            """,
            html)
        #print station
        if station is not None and 'linkid' in station:
            excelurl = baseurl + 'data_'+ station['linkid'] +'_N_WEEK.xls'
            print excelurl
            book = xlrd.open_workbook(file_contents=urllib.urlopen(excelurl).read())
            if book:
                sheet = book.sheets()[0]
                if sheet.ncols == 2 and sheet.nrows > 0:
                    values = []
                    for rownumber in range(3, sheet.nrows): # skip first 3 rows
                        (datecell, numcell) = [ sheet.cell(rownumber, j)  for j in range(sheet.ncols) ]
                        #print "%s, %.1f" % (datecell.value, numcell.value)
                        match = re.match(r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s([0-9]{2}:[0-9]{2})", datecell.value)
                        if match is not None:
                            values.append({
                                'datetime': match.group(3) + '-' + match.group(2) + '-' + match.group(1) + ' ' + match.group(4),
                                'station_id': station['id'],
                                'rain_mm': ("%.1f" % numcell.value),
                                
                            })
                        #print values
                    scraperwiki.sqlite.save(unique_keys=['datetime', 'station_id'], data=values, table_name="raindata")
        else:
            print "WARN: No workable data found."
        #sys.exit()

get_stations()
get_values()# -*- coding: utf-8 -*-

"""
    Aggregator for precipitation data from Hesse/Germany

    Source: Hessisches Landesamt für Umwelt und Geologie
"""

# http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html

import scraperwiki
import mechanize
import re, sys, random
from BeautifulSoup import BeautifulSoup
import scrapemark
import xlrd
import urllib2 as urllib

def shuffle(l):
    """Sort a list in random order"""
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def get_stations():
    """Get meta data about the precipitation sensor stations"""
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html")
    assert br.viewing_html()
    response = br.response()
    soup = BeautifulSoup(response.read())
    tables = soup.findAll('table', attrs={'class': 'contenttable'})
    for table in tables:
        headcolumns = table.findAll('th')
        if len(headcolumns) == 9:
            # correct number of columns - this means we have the right table.
            tbody = table.findAll('tbody')[0]
            rows = []
            # Name, Kurzname, HLUG Messstellennummer, Rechtswert, Hochwert, Geländehöhe, Tagesmessungen seit, Geräte, Betreiber* der Geräte
            fieldnames = ['name', 'shortname', 'id', 'coord_right', 'coord_top', 'altitude', 'since', None, 'operator']
            for tr in tbody.findAll('tr'):
                tds = tr.findAll('td')
                row = {}
                for n in range(0, len(tds)):
                    if fieldnames[n] is not None and tds[n] is not None and tds[n].contents[0] is not None:
                        try:
                            content = str(tds[n].contents[0])
                            content = re.sub(r'<[/]{0,1}[^>]+>', '', content) # remove extra tags
                            content = content.strip()
                            if content != "keine":
                                row[fieldnames[n]] = content
                        except:
                            print "Could not strip field", n, fieldnames[n], tds[n]
                rows.append(row)
                #print row
            #print rows
            scraperwiki.sqlite.save(unique_keys=['id'], data=rows, table_name="stations")

def get_values():
    """Get actual readings from the stations"""
    baseurl = 'http://www.hlug.de/static/pegel/static/'
    listpageurl = baseurl + "list_N_0.htm?entryparakey=N"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(listpageurl)
    assert br.viewing_html()
    links = []
    for link in br.links(url_regex=".*stat_[0-9]+.htm\?entryparakey=N"):
        links.append(link.url)
    links = shuffle(links)
    for link in links:
        subpageurl = baseurl + link
        print "Fetching", subpageurl
        br.open(subpageurl)
        html = br.response().read()
        station = scrapemark.scrape("""
                <table class="wwp_sdheader" cellpadding=4 width=720>
                    <tr>
                        <td class="wwp_sdheader" colspan=6>Station</td>
                    </tr>
                    <tr>
                        <td class="head">Name</td><td class="td1">{{ name }}</td>
                        <td class="head">Messstellen-Nr.</td><td class="td1">{{ id|int }}</td>
                        <td class="head">Flussgebiet</td><td class="td1">{{ river }}</td>
                    </tr>
                </table>
                <a target="_blank" class="graphlink" href="data_{{ linkid }}_N_WEEK.xls">4-Tage</a>
            """,
            html)
        #print station
        if station is not None and 'linkid' in station:
            excelurl = baseurl + 'data_'+ station['linkid'] +'_N_WEEK.xls'
            print excelurl
            book = xlrd.open_workbook(file_contents=urllib.urlopen(excelurl).read())
            if book:
                sheet = book.sheets()[0]
                if sheet.ncols == 2 and sheet.nrows > 0:
                    values = []
                    for rownumber in range(3, sheet.nrows): # skip first 3 rows
                        (datecell, numcell) = [ sheet.cell(rownumber, j)  for j in range(sheet.ncols) ]
                        #print "%s, %.1f" % (datecell.value, numcell.value)
                        match = re.match(r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s([0-9]{2}:[0-9]{2})", datecell.value)
                        if match is not None:
                            values.append({
                                'datetime': match.group(3) + '-' + match.group(2) + '-' + match.group(1) + ' ' + match.group(4),
                                'station_id': station['id'],
                                'rain_mm': ("%.1f" % numcell.value),
                                
                            })
                        #print values
                    scraperwiki.sqlite.save(unique_keys=['datetime', 'station_id'], data=values, table_name="raindata")
        else:
            print "WARN: No workable data found."
        #sys.exit()

get_stations()
get_values()# -*- coding: utf-8 -*-

"""
    Aggregator for precipitation data from Hesse/Germany

    Source: Hessisches Landesamt für Umwelt und Geologie
"""

# http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html

import scraperwiki
import mechanize
import re, sys, random
from BeautifulSoup import BeautifulSoup
import scrapemark
import xlrd
import urllib2 as urllib

def shuffle(l):
    """Sort a list in random order"""
    randomly_tagged_list = [(random.random(), x) for x in l]
    randomly_tagged_list.sort()
    return [x for (r, x) in randomly_tagged_list]

def get_stations():
    """Get meta data about the precipitation sensor stations"""
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("http://www.hlug.de/start/wasser/niederschlag/niederschlagsmessnetz.html")
    assert br.viewing_html()
    response = br.response()
    soup = BeautifulSoup(response.read())
    tables = soup.findAll('table', attrs={'class': 'contenttable'})
    for table in tables:
        headcolumns = table.findAll('th')
        if len(headcolumns) == 9:
            # correct number of columns - this means we have the right table.
            tbody = table.findAll('tbody')[0]
            rows = []
            # Name, Kurzname, HLUG Messstellennummer, Rechtswert, Hochwert, Geländehöhe, Tagesmessungen seit, Geräte, Betreiber* der Geräte
            fieldnames = ['name', 'shortname', 'id', 'coord_right', 'coord_top', 'altitude', 'since', None, 'operator']
            for tr in tbody.findAll('tr'):
                tds = tr.findAll('td')
                row = {}
                for n in range(0, len(tds)):
                    if fieldnames[n] is not None and tds[n] is not None and tds[n].contents[0] is not None:
                        try:
                            content = str(tds[n].contents[0])
                            content = re.sub(r'<[/]{0,1}[^>]+>', '', content) # remove extra tags
                            content = content.strip()
                            if content != "keine":
                                row[fieldnames[n]] = content
                        except:
                            print "Could not strip field", n, fieldnames[n], tds[n]
                rows.append(row)
                #print row
            #print rows
            scraperwiki.sqlite.save(unique_keys=['id'], data=rows, table_name="stations")

def get_values():
    """Get actual readings from the stations"""
    baseurl = 'http://www.hlug.de/static/pegel/static/'
    listpageurl = baseurl + "list_N_0.htm?entryparakey=N"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(listpageurl)
    assert br.viewing_html()
    links = []
    for link in br.links(url_regex=".*stat_[0-9]+.htm\?entryparakey=N"):
        links.append(link.url)
    links = shuffle(links)
    for link in links:
        subpageurl = baseurl + link
        print "Fetching", subpageurl
        br.open(subpageurl)
        html = br.response().read()
        station = scrapemark.scrape("""
                <table class="wwp_sdheader" cellpadding=4 width=720>
                    <tr>
                        <td class="wwp_sdheader" colspan=6>Station</td>
                    </tr>
                    <tr>
                        <td class="head">Name</td><td class="td1">{{ name }}</td>
                        <td class="head">Messstellen-Nr.</td><td class="td1">{{ id|int }}</td>
                        <td class="head">Flussgebiet</td><td class="td1">{{ river }}</td>
                    </tr>
                </table>
                <a target="_blank" class="graphlink" href="data_{{ linkid }}_N_WEEK.xls">4-Tage</a>
            """,
            html)
        #print station
        if station is not None and 'linkid' in station:
            excelurl = baseurl + 'data_'+ station['linkid'] +'_N_WEEK.xls'
            print excelurl
            book = xlrd.open_workbook(file_contents=urllib.urlopen(excelurl).read())
            if book:
                sheet = book.sheets()[0]
                if sheet.ncols == 2 and sheet.nrows > 0:
                    values = []
                    for rownumber in range(3, sheet.nrows): # skip first 3 rows
                        (datecell, numcell) = [ sheet.cell(rownumber, j)  for j in range(sheet.ncols) ]
                        #print "%s, %.1f" % (datecell.value, numcell.value)
                        match = re.match(r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\s([0-9]{2}:[0-9]{2})", datecell.value)
                        if match is not None:
                            values.append({
                                'datetime': match.group(3) + '-' + match.group(2) + '-' + match.group(1) + ' ' + match.group(4),
                                'station_id': station['id'],
                                'rain_mm': ("%.1f" % numcell.value),
                                
                            })
                        #print values
                    scraperwiki.sqlite.save(unique_keys=['datetime', 'station_id'], data=values, table_name="raindata")
        else:
            print "WARN: No workable data found."
        #sys.exit()

get_stations()
get_values()