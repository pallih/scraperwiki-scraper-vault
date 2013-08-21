import mechanize
import scraperwiki
import re
import datetime
import urlparse
import urllib
import urllib2
import sqlite3
import tempfile


def parsepage(html):
    mtable = re.search('(?s)<table class="results" border="1" align="center">(.*?)</table>', html)
    table = mtable.group(1)
    rows = re.findall('(?s)<tr.*?>(.*?)</tr>', table)
    headings = [ ]
    for col in re.findall('(?s)<td.*?>(.*?)</td>', rows[0]):
        h = re.sub("<.*?>", "", col)
        h = re.sub("&nbsp;", " ", h)
        headings.append(h.strip())
        
    assert headings == ['Fund', 'Last', 'First', 'Final Employer', 'Retire Date', 
                        'Annual Pension', 'Final Avg. Salary', 'Enroll Date', 
                        'Residence'], headings
    
    for row in rows[1:]:
        cols = re.findall('(?s)<td.*?><p class="style19">(.*?)(?:&nbsp;|\s)*</p></td>', row)
        assert len(headings) == len(cols), [cols, row, headings]
        data = dict(zip(headings, cols))
        #print data
        if (data['Final Avg. Salary'], data['Retire Date'], data['Residence'], data['Enroll Date']) == ('$0.00', '12/31/1969', '', ''):
            return 0
    
        last = data.pop("Last")
        mlastname = re.match('<a href="details2.php\?recordID=(\d+)" class="style5">(.*?)', last)
        assert mlastname, last
    
        data["recordid"] = mlastname.group(1)
        data["lastname"] = mlastname.group(2)

        data["url"] = "http://php.app.com/njretire07/details2.php?recordID="+data["recordid"]   # veteran status is on this page, but not collected

        firstname = data.pop("First")
        firstname = re.sub("(&nbsp;|\s)+", " ", firstname)
        data["firstname"] = firstname.strip()

        data["fund"] = re.sub("(&nbsp;|\s|\xa0)+", " ", data.pop("Fund"))
        
        annualpension = data.pop('Annual Pension')
        assert annualpension[0] == '$', annualpension
        data['annualpension'] = re.sub(",", "", annualpension[1:])
        
        finalsalary = data.pop('Final Avg. Salary')
        assert finalsalary[0] == '$', finalsalary
        data['finalsalary'] = re.sub(",", "", finalsalary[1:])

        # '07/01/1980' format
        dateretire = data.pop('Retire Date')
        mdateretire = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', dateretire)
        data["dateretire"] = datetime.date(int(mdateretire.group(3)), int(mdateretire.group(2)), int(mdateretire.group(1)))
        
        # '1971-01-00' format. (suppress day=0)
        dateenroll = data.pop('Enroll Date')
        mdateretire = re.match('(\d\d\d\d)-(\d\d)-(\d\d)', dateenroll)
        if mdateretire.group(1) != '0000':
            data["dateenroll"] = datetime.date(int(mdateretire.group(1)), 
                                               max(1, int(mdateretire.group(2))), 
                                               max(1, int(mdateretire.group(3))))
        data["year"] = data["dateretire"].year
        
        #print data
        scraperwiki.sqlite.save(unique_keys=["recordid"], data=data)        
    return len(rows) - 1    


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Armed Forces oversees', 'Armed Forces Pacific', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico ', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands ', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

years = ['2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961', '1960', '1959', '1958', '1957', '1954']


    
def scrapeyearstate(year, state):
    print year, state
    url = "http://php.app.com/njretire07/"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(name="form1")
    usstatecontrol = br.form.find_control("name")
    retiredyearcontrol = br.form.find_control("ret_yr")

    stateitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(usstatecontrol.items[:])]
    #print stateitems
    #yearitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(retiredyearcontrol.items[1:])]
    lstates = [str(item)  for item in list(usstatecontrol.items[2:])]
    lyears = [str(item)  for item in list(retiredyearcontrol.items[1:])]

    if state != 'All':
        br["name"] = [state]  # ["Florida"]
    br["ret_yr"] = [year] # ["1980"]
    response = br.submit()
    html = response.read()
    parsepage(html)

    
    # derive and parse the rest of the pages
    # /njretire07/results2.php?pageNum_Recordset1=18&totalRows_Recordset1=186&lastn=&firstn=&location=%25&FundName=%25&ret_yr=1980&name=Florida&Submit=Search
    mlast = re.search('<span class="style25"><a href="(/njretire07/results2.php.*?)">Last</a>', html)
    if mlast:
        lastlink = mlast.group(1)
        lastlink = re.sub("&amp;", "&", lastlink)
        nrecordsets = re.search('pageNum_Recordset1=(\d+)', lastlink).group(1)
        print nrecordsets
        
        for recordset in range(1, int(nrecordsets)+1):
            nlink = re.sub('pageNum_Recordset1=\d+', 'pageNum_Recordset1=%d' % recordset, lastlink)
            purl = urlparse.urljoin(url, nlink)
            print recordset, purl
            phtml = urllib2.urlopen(purl).read()
            parsepage(phtml)
                    



# these are the missing years so far
for year in range(1986, 2009):
    for state in states[:]:
        scrapeyearstate("%s" % year, state)
    #scrapeyearstate("%s" % year, 'All')
    break
    
    

import mechanize
import scraperwiki
import re
import datetime
import urlparse
import urllib
import urllib2
import sqlite3
import tempfile


def parsepage(html):
    mtable = re.search('(?s)<table class="results" border="1" align="center">(.*?)</table>', html)
    table = mtable.group(1)
    rows = re.findall('(?s)<tr.*?>(.*?)</tr>', table)
    headings = [ ]
    for col in re.findall('(?s)<td.*?>(.*?)</td>', rows[0]):
        h = re.sub("<.*?>", "", col)
        h = re.sub("&nbsp;", " ", h)
        headings.append(h.strip())
        
    assert headings == ['Fund', 'Last', 'First', 'Final Employer', 'Retire Date', 
                        'Annual Pension', 'Final Avg. Salary', 'Enroll Date', 
                        'Residence'], headings
    
    for row in rows[1:]:
        cols = re.findall('(?s)<td.*?><p class="style19">(.*?)(?:&nbsp;|\s)*</p></td>', row)
        assert len(headings) == len(cols), [cols, row, headings]
        data = dict(zip(headings, cols))
        #print data
        if (data['Final Avg. Salary'], data['Retire Date'], data['Residence'], data['Enroll Date']) == ('$0.00', '12/31/1969', '', ''):
            return 0
    
        last = data.pop("Last")
        mlastname = re.match('<a href="details2.php\?recordID=(\d+)" class="style5">(.*?)', last)
        assert mlastname, last
    
        data["recordid"] = mlastname.group(1)
        data["lastname"] = mlastname.group(2)

        data["url"] = "http://php.app.com/njretire07/details2.php?recordID="+data["recordid"]   # veteran status is on this page, but not collected

        firstname = data.pop("First")
        firstname = re.sub("(&nbsp;|\s)+", " ", firstname)
        data["firstname"] = firstname.strip()

        data["fund"] = re.sub("(&nbsp;|\s|\xa0)+", " ", data.pop("Fund"))
        
        annualpension = data.pop('Annual Pension')
        assert annualpension[0] == '$', annualpension
        data['annualpension'] = re.sub(",", "", annualpension[1:])
        
        finalsalary = data.pop('Final Avg. Salary')
        assert finalsalary[0] == '$', finalsalary
        data['finalsalary'] = re.sub(",", "", finalsalary[1:])

        # '07/01/1980' format
        dateretire = data.pop('Retire Date')
        mdateretire = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', dateretire)
        data["dateretire"] = datetime.date(int(mdateretire.group(3)), int(mdateretire.group(2)), int(mdateretire.group(1)))
        
        # '1971-01-00' format. (suppress day=0)
        dateenroll = data.pop('Enroll Date')
        mdateretire = re.match('(\d\d\d\d)-(\d\d)-(\d\d)', dateenroll)
        if mdateretire.group(1) != '0000':
            data["dateenroll"] = datetime.date(int(mdateretire.group(1)), 
                                               max(1, int(mdateretire.group(2))), 
                                               max(1, int(mdateretire.group(3))))
        data["year"] = data["dateretire"].year
        
        #print data
        scraperwiki.sqlite.save(unique_keys=["recordid"], data=data)        
    return len(rows) - 1    


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Armed Forces oversees', 'Armed Forces Pacific', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico ', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands ', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

years = ['2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961', '1960', '1959', '1958', '1957', '1954']


    
def scrapeyearstate(year, state):
    print year, state
    url = "http://php.app.com/njretire07/"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(name="form1")
    usstatecontrol = br.form.find_control("name")
    retiredyearcontrol = br.form.find_control("ret_yr")

    stateitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(usstatecontrol.items[:])]
    #print stateitems
    #yearitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(retiredyearcontrol.items[1:])]
    lstates = [str(item)  for item in list(usstatecontrol.items[2:])]
    lyears = [str(item)  for item in list(retiredyearcontrol.items[1:])]

    if state != 'All':
        br["name"] = [state]  # ["Florida"]
    br["ret_yr"] = [year] # ["1980"]
    response = br.submit()
    html = response.read()
    parsepage(html)

    
    # derive and parse the rest of the pages
    # /njretire07/results2.php?pageNum_Recordset1=18&totalRows_Recordset1=186&lastn=&firstn=&location=%25&FundName=%25&ret_yr=1980&name=Florida&Submit=Search
    mlast = re.search('<span class="style25"><a href="(/njretire07/results2.php.*?)">Last</a>', html)
    if mlast:
        lastlink = mlast.group(1)
        lastlink = re.sub("&amp;", "&", lastlink)
        nrecordsets = re.search('pageNum_Recordset1=(\d+)', lastlink).group(1)
        print nrecordsets
        
        for recordset in range(1, int(nrecordsets)+1):
            nlink = re.sub('pageNum_Recordset1=\d+', 'pageNum_Recordset1=%d' % recordset, lastlink)
            purl = urlparse.urljoin(url, nlink)
            print recordset, purl
            phtml = urllib2.urlopen(purl).read()
            parsepage(phtml)
                    



# these are the missing years so far
for year in range(1986, 2009):
    for state in states[:]:
        scrapeyearstate("%s" % year, state)
    #scrapeyearstate("%s" % year, 'All')
    break
    
    

import mechanize
import scraperwiki
import re
import datetime
import urlparse
import urllib
import urllib2
import sqlite3
import tempfile


def parsepage(html):
    mtable = re.search('(?s)<table class="results" border="1" align="center">(.*?)</table>', html)
    table = mtable.group(1)
    rows = re.findall('(?s)<tr.*?>(.*?)</tr>', table)
    headings = [ ]
    for col in re.findall('(?s)<td.*?>(.*?)</td>', rows[0]):
        h = re.sub("<.*?>", "", col)
        h = re.sub("&nbsp;", " ", h)
        headings.append(h.strip())
        
    assert headings == ['Fund', 'Last', 'First', 'Final Employer', 'Retire Date', 
                        'Annual Pension', 'Final Avg. Salary', 'Enroll Date', 
                        'Residence'], headings
    
    for row in rows[1:]:
        cols = re.findall('(?s)<td.*?><p class="style19">(.*?)(?:&nbsp;|\s)*</p></td>', row)
        assert len(headings) == len(cols), [cols, row, headings]
        data = dict(zip(headings, cols))
        #print data
        if (data['Final Avg. Salary'], data['Retire Date'], data['Residence'], data['Enroll Date']) == ('$0.00', '12/31/1969', '', ''):
            return 0
    
        last = data.pop("Last")
        mlastname = re.match('<a href="details2.php\?recordID=(\d+)" class="style5">(.*?)', last)
        assert mlastname, last
    
        data["recordid"] = mlastname.group(1)
        data["lastname"] = mlastname.group(2)

        data["url"] = "http://php.app.com/njretire07/details2.php?recordID="+data["recordid"]   # veteran status is on this page, but not collected

        firstname = data.pop("First")
        firstname = re.sub("(&nbsp;|\s)+", " ", firstname)
        data["firstname"] = firstname.strip()

        data["fund"] = re.sub("(&nbsp;|\s|\xa0)+", " ", data.pop("Fund"))
        
        annualpension = data.pop('Annual Pension')
        assert annualpension[0] == '$', annualpension
        data['annualpension'] = re.sub(",", "", annualpension[1:])
        
        finalsalary = data.pop('Final Avg. Salary')
        assert finalsalary[0] == '$', finalsalary
        data['finalsalary'] = re.sub(",", "", finalsalary[1:])

        # '07/01/1980' format
        dateretire = data.pop('Retire Date')
        mdateretire = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', dateretire)
        data["dateretire"] = datetime.date(int(mdateretire.group(3)), int(mdateretire.group(2)), int(mdateretire.group(1)))
        
        # '1971-01-00' format. (suppress day=0)
        dateenroll = data.pop('Enroll Date')
        mdateretire = re.match('(\d\d\d\d)-(\d\d)-(\d\d)', dateenroll)
        if mdateretire.group(1) != '0000':
            data["dateenroll"] = datetime.date(int(mdateretire.group(1)), 
                                               max(1, int(mdateretire.group(2))), 
                                               max(1, int(mdateretire.group(3))))
        data["year"] = data["dateretire"].year
        
        #print data
        scraperwiki.sqlite.save(unique_keys=["recordid"], data=data)        
    return len(rows) - 1    


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Armed Forces oversees', 'Armed Forces Pacific', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico ', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands ', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

years = ['2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961', '1960', '1959', '1958', '1957', '1954']


    
def scrapeyearstate(year, state):
    print year, state
    url = "http://php.app.com/njretire07/"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(name="form1")
    usstatecontrol = br.form.find_control("name")
    retiredyearcontrol = br.form.find_control("ret_yr")

    stateitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(usstatecontrol.items[:])]
    #print stateitems
    #yearitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(retiredyearcontrol.items[1:])]
    lstates = [str(item)  for item in list(usstatecontrol.items[2:])]
    lyears = [str(item)  for item in list(retiredyearcontrol.items[1:])]

    if state != 'All':
        br["name"] = [state]  # ["Florida"]
    br["ret_yr"] = [year] # ["1980"]
    response = br.submit()
    html = response.read()
    parsepage(html)

    
    # derive and parse the rest of the pages
    # /njretire07/results2.php?pageNum_Recordset1=18&totalRows_Recordset1=186&lastn=&firstn=&location=%25&FundName=%25&ret_yr=1980&name=Florida&Submit=Search
    mlast = re.search('<span class="style25"><a href="(/njretire07/results2.php.*?)">Last</a>', html)
    if mlast:
        lastlink = mlast.group(1)
        lastlink = re.sub("&amp;", "&", lastlink)
        nrecordsets = re.search('pageNum_Recordset1=(\d+)', lastlink).group(1)
        print nrecordsets
        
        for recordset in range(1, int(nrecordsets)+1):
            nlink = re.sub('pageNum_Recordset1=\d+', 'pageNum_Recordset1=%d' % recordset, lastlink)
            purl = urlparse.urljoin(url, nlink)
            print recordset, purl
            phtml = urllib2.urlopen(purl).read()
            parsepage(phtml)
                    



# these are the missing years so far
for year in range(1986, 2009):
    for state in states[:]:
        scrapeyearstate("%s" % year, state)
    #scrapeyearstate("%s" % year, 'All')
    break
    
    

import mechanize
import scraperwiki
import re
import datetime
import urlparse
import urllib
import urllib2
import sqlite3
import tempfile


def parsepage(html):
    mtable = re.search('(?s)<table class="results" border="1" align="center">(.*?)</table>', html)
    table = mtable.group(1)
    rows = re.findall('(?s)<tr.*?>(.*?)</tr>', table)
    headings = [ ]
    for col in re.findall('(?s)<td.*?>(.*?)</td>', rows[0]):
        h = re.sub("<.*?>", "", col)
        h = re.sub("&nbsp;", " ", h)
        headings.append(h.strip())
        
    assert headings == ['Fund', 'Last', 'First', 'Final Employer', 'Retire Date', 
                        'Annual Pension', 'Final Avg. Salary', 'Enroll Date', 
                        'Residence'], headings
    
    for row in rows[1:]:
        cols = re.findall('(?s)<td.*?><p class="style19">(.*?)(?:&nbsp;|\s)*</p></td>', row)
        assert len(headings) == len(cols), [cols, row, headings]
        data = dict(zip(headings, cols))
        #print data
        if (data['Final Avg. Salary'], data['Retire Date'], data['Residence'], data['Enroll Date']) == ('$0.00', '12/31/1969', '', ''):
            return 0
    
        last = data.pop("Last")
        mlastname = re.match('<a href="details2.php\?recordID=(\d+)" class="style5">(.*?)', last)
        assert mlastname, last
    
        data["recordid"] = mlastname.group(1)
        data["lastname"] = mlastname.group(2)

        data["url"] = "http://php.app.com/njretire07/details2.php?recordID="+data["recordid"]   # veteran status is on this page, but not collected

        firstname = data.pop("First")
        firstname = re.sub("(&nbsp;|\s)+", " ", firstname)
        data["firstname"] = firstname.strip()

        data["fund"] = re.sub("(&nbsp;|\s|\xa0)+", " ", data.pop("Fund"))
        
        annualpension = data.pop('Annual Pension')
        assert annualpension[0] == '$', annualpension
        data['annualpension'] = re.sub(",", "", annualpension[1:])
        
        finalsalary = data.pop('Final Avg. Salary')
        assert finalsalary[0] == '$', finalsalary
        data['finalsalary'] = re.sub(",", "", finalsalary[1:])

        # '07/01/1980' format
        dateretire = data.pop('Retire Date')
        mdateretire = re.match('(\d\d)/(\d\d)/(\d\d\d\d)', dateretire)
        data["dateretire"] = datetime.date(int(mdateretire.group(3)), int(mdateretire.group(2)), int(mdateretire.group(1)))
        
        # '1971-01-00' format. (suppress day=0)
        dateenroll = data.pop('Enroll Date')
        mdateretire = re.match('(\d\d\d\d)-(\d\d)-(\d\d)', dateenroll)
        if mdateretire.group(1) != '0000':
            data["dateenroll"] = datetime.date(int(mdateretire.group(1)), 
                                               max(1, int(mdateretire.group(2))), 
                                               max(1, int(mdateretire.group(3))))
        data["year"] = data["dateretire"].year
        
        #print data
        scraperwiki.sqlite.save(unique_keys=["recordid"], data=data)        
    return len(rows) - 1    


states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Armed Forces oversees', 'Armed Forces Pacific', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico ', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virgin Islands ', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

years = ['2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974', '1973', '1972', '1971', '1970', '1969', '1968', '1967', '1966', '1965', '1964', '1963', '1962', '1961', '1960', '1959', '1958', '1957', '1954']


    
def scrapeyearstate(year, state):
    print year, state
    url = "http://php.app.com/njretire07/"
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(url)
    br.select_form(name="form1")
    usstatecontrol = br.form.find_control("name")
    retiredyearcontrol = br.form.find_control("ret_yr")

    stateitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(usstatecontrol.items[:])]
    #print stateitems
    #yearitems = [(str(item), [label.text  for label in item.get_labels()])  for item in list(retiredyearcontrol.items[1:])]
    lstates = [str(item)  for item in list(usstatecontrol.items[2:])]
    lyears = [str(item)  for item in list(retiredyearcontrol.items[1:])]

    if state != 'All':
        br["name"] = [state]  # ["Florida"]
    br["ret_yr"] = [year] # ["1980"]
    response = br.submit()
    html = response.read()
    parsepage(html)

    
    # derive and parse the rest of the pages
    # /njretire07/results2.php?pageNum_Recordset1=18&totalRows_Recordset1=186&lastn=&firstn=&location=%25&FundName=%25&ret_yr=1980&name=Florida&Submit=Search
    mlast = re.search('<span class="style25"><a href="(/njretire07/results2.php.*?)">Last</a>', html)
    if mlast:
        lastlink = mlast.group(1)
        lastlink = re.sub("&amp;", "&", lastlink)
        nrecordsets = re.search('pageNum_Recordset1=(\d+)', lastlink).group(1)
        print nrecordsets
        
        for recordset in range(1, int(nrecordsets)+1):
            nlink = re.sub('pageNum_Recordset1=\d+', 'pageNum_Recordset1=%d' % recordset, lastlink)
            purl = urlparse.urljoin(url, nlink)
            print recordset, purl
            phtml = urllib2.urlopen(purl).read()
            parsepage(phtml)
                    



# these are the missing years so far
for year in range(1986, 2009):
    for state in states[:]:
        scrapeyearstate("%s" % year, state)
    #scrapeyearstate("%s" % year, 'All')
    break
    
    

