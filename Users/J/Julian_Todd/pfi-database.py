import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600import urllib
import re
import scraperwiki
import datetime

# The visualisation can be done from http://scraperwiki.com/scrapers/show/pfi-visualisation/

# this method only gets 840 out of the 920.  Maybe improve later
def GetPFInums():
    url = "http://www.partnershipsuk.org.uk/puk-projects-database-search.aspx"
    html = urllib.urlopen(url).read()
    regions = re.findall("href='PUK-Projects-Database-Map.aspx\?Region=(.*?)'", html)
    allpfinums = [ ]
    for region in regions:
        urlregion = "http://www.partnershipsuk.org.uk/PUK-Projects-Database-Map.aspx?Region=%s" % region
        html = urllib.urlopen(urlregion).read()
        pfinums = re.findall("Project=(.*?)'", html)
        allpfinums.extend(pfinums)
        #break
    return allpfinums

datedfields = {"Date of Financial Close":"DateFinancialClose", "OJEU/OJEC Date":"DateOJEC", "Operational From":"DateOperational", "Planned Date of Operation":"DatePlannedOperational"}

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ] 


def ConvertAdvisors(advisors):
    padvisors = advisors
    lpadvisors = [ ]
    for padvisor in padvisors.split('<br/>'):
        if padvisor:
            lpadvisor = padvisor.split('-')[0].strip()   # second is their speciality
            lpadvisors.append(lpadvisor)
    return lpadvisors

def ConvertList(ll):
    if not ll:
        return []
    r = [ ]
    for l in ll.split('<br/>'):
        if l:
            r.append(l)
    return r


def CleanupData(data):
    # clean up dates
    for datedfield, newdatedfield in datedfields.iteritems():
        datedvalue = data.pop(datedfield, None)
        if datedvalue:
            mdate = re.match('(\d\d) (\w+) (\d\d\d\d)$', datedvalue)
            assert mdate, [datedvalue]
            day = int(mdate.group(1))
            month = months.index(mdate.group(2)) + 1
            year = int(mdate.group(3))
            data[newdatedfield] = datetime.date(year, month, day)

    members = data.pop('Shareholders / Members / Partners', '')
    lmembers = [ ]
    for member in members.split('<br/>'):
        if member:
            smember = member.split('<br>')  # Normally - name, 41%, From: , To: Present
            lmembers.append(smember[0])
    print lmembers
    data['members'] = lmembers

    contractor = data.pop('Contractor / Consortium / Partnership / JV', '')
    data['contractor'] = contractor

    data['department'] = data.pop('Central GovernmentSponsor Department(s)', '')

    data['private advisors'] = ConvertAdvisors(data.pop('Private Sector Advisor(s)', ''))
    data['advisors'] = ConvertAdvisors(data.pop('Public Sector Authority Advisor(s)', ''))
    data['private contractors'] = ConvertAdvisors(data.pop('Private Sector Contractor(s)', ''))
    data['banks'] = ConvertList(data.pop('Principal Bank(s) / Bond Arranger(s)', ''))
    data['authority'] = ConvertList(data.pop('Public Sector Authority / Commissioning Body', ''))
    data['constituency'] = [ c.strip()  for c in data.pop('Constituency', '').split(',')  if c ] 
             
    
def ScrapeOneProject(pfinumber):
    url = "http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=%s" % pfinumber
    html = urllib.urlopen(url).read()
    fields = re.findall('(?s)<tr>\s*<td width="50%">(.*?)\s*</td><td>(.*?)</td>', html)
    rawdata = dict(fields)
    rawdata["pfinumber"] = pfinumber
    rawdata["url"] = url
    CleanupData(rawdata)
    print rawdata 
    scraperwiki.sqlite.save(unique_keys=["pfinumber"], data=rawdata)


def Main():    
    allpfinums = GetPFInums()
    print len(allpfinums)
    print allpfinums
    for pfinumber in allpfinums:
        for i in range(3):
            try:
                ScrapeOneProject(pfinumber)
                break
            except IOError:
                pass
        else:
            print "Failed with:", pfinumber

Main()
ScrapeOneProject(11600)
#http://www.partnershipsuk.org.uk/PUK-Case-Study.aspx?Project=11600