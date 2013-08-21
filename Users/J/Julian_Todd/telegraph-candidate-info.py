import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, string

mpnamecorrections = { 'Philip Lee':'Phillip Lee', 'Peter Wishart':'Pete Wishart', 'Robert Neill':'Bob Neill', 
                      'Sir Robert Smith':'Robert Smith', 'Nicholas Brown':'Nick Brown', 'Ed Miliband':'Edward Miliband', 
                      'Edward Garnier QC':'Edward Garnier', 'Huw Irranca Davies':'Huw Irranca-Davies', 
                      'Ian Paisley':'Ian Paisley Jnr', 'Susan Jones':'Susan Elan Jones', 'Sir Menzies Campbell':'Menzies Campbell', 
                      'Sian James':u'Si\xe2n James' }
cnamecorrections = {"Plymouth Sutton & Devonport":"Plymouth, Sutton and Devonport", "Cotswolds, The":"The Cotswolds", 
                    "Plymouth Moor View":"Plymouth, Moor View" }

scraperwiki.sqlite.attach("parlparse")
def updateidvals(mpdata):
    ssql = "* from constituencynames left join constituencies on constituencies.id=constituency_id where text like ?" +\
           " and fromdate <= '2010-05-06' and todate > '2010-05-06' group by constituency_id"
    cname = mpdata["Constituency"].strip()
    cname = cnamecorrections.get(cname, cname)
    result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    if len(result) == 0:
        cname = cname.replace("&", "and")
        result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    assert len(result) == 1, (cname, result)
    mpdata["Constituency_id"] = result[0]["constituency_id"]

    if mpdata.get('status') == 'ELECTED MP 2010':
        mpname = mpdata["mpname"]
        ssql = "* from members where (firstname||' '||lastname) like ? and fromdate = '2010-05-06'"
        mpname = mpnamecorrections.get(mpname, mpname)
        result = scraperwiki.sqlite.select(ssql, mpname, verbose=0)
            # >= date because of Anne McIntosh
        if len(result) == 0:
            ssql = "* from members where lastname like ? and fromdate >= '2010-05-06'"   
            result = scraperwiki.sqlite.select(ssql, mpname.split()[-1], verbose=0)
            if len(result) == 1:
                print "Renaming %s as %s %s" % (mpname, result[0]["firstname"], result[0]["lastname"])
        assert len(result) == 1, (mpname, result)
        mpdata["mp_id"] = result[0]["id"]


def Main():
    #url = "http://ukpolitics.telegraph.co.uk/Bristol+West/Paul+Smith"
    #SingleMPpage(url, "P")
    for letter in "LMNOPQRSTUVWXYZ": # string.ascii_uppercase[16:]:
        candidatesforletter = GetCandidatesForLetter(letter)
        mcandidatesforletter = scraperwiki.sqlite.select("count(*) as c from swdata where letter=?", letter)[0]["c"]
        print "%d candidates on letter: %s, has %d" % (len(candidatesforletter), letter, mcandidatesforletter)
        if mcandidatesforletter == len(candidatesforletter):
            print "skipping"
            continue
        donestart = scraperwiki.sqlite.get_var("done_"+letter, 0)
        print "Starting at: ", donestart
        for i in range(donestart, len(candidatesforletter)):
            curl, name = candidatesforletter[i]
            SingleMPpage(curl, letter)
            scraperwiki.sqlite.save_var("done_"+letter, i, verbose=0)


def SingleMPpage(url, letter):
    root = RootLxml(url)
    if root is None:
        return   # bail out.  lots of data already

    mpdata = { "letter":letter }
    mpdata['mpname'] = root.cssselect('div.headerArea h1')[0].text
    mpdata['url'] = url

    lparty = root.cssselect('div#party p')
    if lparty:
        mpdata['party'] = lparty[0].text.strip(', \t\n')
    else:
        print "Party missing", url

    mpdata['education'] = [ ]
    for table in root.cssselect('table.electionTable'):
        rows = table.cssselect('tr')
        caption = rows[0].cssselect('th div.caption')[0].text
        for row in rows[1:]:
            stype = row[0].text.strip()
            if len(row) == 2:
                sname = row[1].text.strip()
            else:
                sname = stype
                stype = ""
            if sname:
                mpdata['education'].append({'level':caption, 'type':stype, 'name':sname})
    
    lstatus = root.cssselect('div.headerArea div.mpStatus')
    if lstatus:
        mpdata['status'] = lstatus[0].text.strip()
        assert mpdata['status'] == 'ELECTED MP 2010', mpdata


    electioncontent = root.cssselect('div#electionContent')[0]
    edata = { }
    for dl in root.cssselect('div#electionContent div.gutterUnder dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                edata[key] = dtd
                #print key, lxml.etree.tostring(dtd)
            # re.sub('</?dd[^>]*>', '', lxml.etree.tostring(dtd)).strip()
    assert set(['Sector', 'Votes', 'Detail', 'Majority', 'Position', 'Constituency', "MPs' Expenses"]).issuperset(edata.keys()), edata
    mpdata["employmentsector"] = edata["Sector"].text.strip()
    mpdata["Votes"] = int(edata["Votes"].text.replace(",", ""))
    mpdata["VotePosition"] = int(edata["Position"].text)
    mpdata["Constituency"] = edata["Constituency"][0].text
    mpdata["ConstituencyURL"] = urlparse.urljoin(url, edata["Constituency"][0].attrib.get('href'))
    if "MPs' Expenses" in edata:
        mpdata['expenses'] = edata["MPs' Expenses"][0].attrib.get('href')
    
    odata = { }
    for dl in root.cssselect('div#overview dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                sdtd = lxml.etree.tostring(dtd)
                if re.search('twitter.com', sdtd):
                    odata['twitter'] = dtd
                elif re.search('Facebook group', sdtd):
                    odata['facebook'] = dtd
                else:
                    odata[key] = dtd
                #print key, lxml.etree.tostring(dtd)

    if "Gender" in odata:
        mpdata["gender"] = odata["Gender"].text
    if "Age" in odata:
        mpdata["age"] = int(odata["Age"].text)
    if 'Email' in mpdata:
        mpdata["Email"] = odata["Email"][0].text
    if 'Web' in odata:
        mpdata["webpage"] = odata["Web"][0].attrib.get('href')
    if 'facebook' in odata:
        mpdata["facebook"] = odata["facebook"][0].attrib.get('href')
    if 'twitter' in odata:
        mpdata["twitter"] = odata["twitter"][0].attrib.get('href')

    imagesel = root.cssselect('img.fullCandidateImage')
    if imagesel:
        imagesrc = imagesel[0].attrib.get('src')
        if imagesrc != "http://www.telegraph.co.uk/telegraph/multimedia/archive/01616/silhouette_140_1616987a.jpg":
            mpdata['image'] = imagesrc


    # fill in specific education fields so it is not a list for easier lookup
    for ieducation in mpdata['education']:
        mpdata['education-'+ieducation['level']] = ieducation ['type']

    updateidvals(mpdata)
    scraperwiki.datastore.save(unique_keys=["mpname", "Constituency"], data=mpdata)



def RootLxml(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            if root is not None:
                return root
        except:
            pass
    print "Failed to download", url
    #print urllib.urlopen(url).read()
    return None
        
    


def GetCandidatesForLetter(letter):
    url = "http://ukpolitics.telegraph.co.uk/a-z/candidates/" + letter
    root = RootLxml(url)
    result = [ ]
    atags = root.cssselect('ul.azList li a')
    for i in range(0, len(atags)):
        a = atags[i]
        relativelink = a.attrib.get('href')
        candidatename = a.text
        absolutelink = urlparse.urljoin(url, relativelink)
        result.append((absolutelink, candidatename))
    return result


Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, string

mpnamecorrections = { 'Philip Lee':'Phillip Lee', 'Peter Wishart':'Pete Wishart', 'Robert Neill':'Bob Neill', 
                      'Sir Robert Smith':'Robert Smith', 'Nicholas Brown':'Nick Brown', 'Ed Miliband':'Edward Miliband', 
                      'Edward Garnier QC':'Edward Garnier', 'Huw Irranca Davies':'Huw Irranca-Davies', 
                      'Ian Paisley':'Ian Paisley Jnr', 'Susan Jones':'Susan Elan Jones', 'Sir Menzies Campbell':'Menzies Campbell', 
                      'Sian James':u'Si\xe2n James' }
cnamecorrections = {"Plymouth Sutton & Devonport":"Plymouth, Sutton and Devonport", "Cotswolds, The":"The Cotswolds", 
                    "Plymouth Moor View":"Plymouth, Moor View" }

scraperwiki.sqlite.attach("parlparse")
def updateidvals(mpdata):
    ssql = "* from constituencynames left join constituencies on constituencies.id=constituency_id where text like ?" +\
           " and fromdate <= '2010-05-06' and todate > '2010-05-06' group by constituency_id"
    cname = mpdata["Constituency"].strip()
    cname = cnamecorrections.get(cname, cname)
    result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    if len(result) == 0:
        cname = cname.replace("&", "and")
        result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    assert len(result) == 1, (cname, result)
    mpdata["Constituency_id"] = result[0]["constituency_id"]

    if mpdata.get('status') == 'ELECTED MP 2010':
        mpname = mpdata["mpname"]
        ssql = "* from members where (firstname||' '||lastname) like ? and fromdate = '2010-05-06'"
        mpname = mpnamecorrections.get(mpname, mpname)
        result = scraperwiki.sqlite.select(ssql, mpname, verbose=0)
            # >= date because of Anne McIntosh
        if len(result) == 0:
            ssql = "* from members where lastname like ? and fromdate >= '2010-05-06'"   
            result = scraperwiki.sqlite.select(ssql, mpname.split()[-1], verbose=0)
            if len(result) == 1:
                print "Renaming %s as %s %s" % (mpname, result[0]["firstname"], result[0]["lastname"])
        assert len(result) == 1, (mpname, result)
        mpdata["mp_id"] = result[0]["id"]


def Main():
    #url = "http://ukpolitics.telegraph.co.uk/Bristol+West/Paul+Smith"
    #SingleMPpage(url, "P")
    for letter in "LMNOPQRSTUVWXYZ": # string.ascii_uppercase[16:]:
        candidatesforletter = GetCandidatesForLetter(letter)
        mcandidatesforletter = scraperwiki.sqlite.select("count(*) as c from swdata where letter=?", letter)[0]["c"]
        print "%d candidates on letter: %s, has %d" % (len(candidatesforletter), letter, mcandidatesforletter)
        if mcandidatesforletter == len(candidatesforletter):
            print "skipping"
            continue
        donestart = scraperwiki.sqlite.get_var("done_"+letter, 0)
        print "Starting at: ", donestart
        for i in range(donestart, len(candidatesforletter)):
            curl, name = candidatesforletter[i]
            SingleMPpage(curl, letter)
            scraperwiki.sqlite.save_var("done_"+letter, i, verbose=0)


def SingleMPpage(url, letter):
    root = RootLxml(url)
    if root is None:
        return   # bail out.  lots of data already

    mpdata = { "letter":letter }
    mpdata['mpname'] = root.cssselect('div.headerArea h1')[0].text
    mpdata['url'] = url

    lparty = root.cssselect('div#party p')
    if lparty:
        mpdata['party'] = lparty[0].text.strip(', \t\n')
    else:
        print "Party missing", url

    mpdata['education'] = [ ]
    for table in root.cssselect('table.electionTable'):
        rows = table.cssselect('tr')
        caption = rows[0].cssselect('th div.caption')[0].text
        for row in rows[1:]:
            stype = row[0].text.strip()
            if len(row) == 2:
                sname = row[1].text.strip()
            else:
                sname = stype
                stype = ""
            if sname:
                mpdata['education'].append({'level':caption, 'type':stype, 'name':sname})
    
    lstatus = root.cssselect('div.headerArea div.mpStatus')
    if lstatus:
        mpdata['status'] = lstatus[0].text.strip()
        assert mpdata['status'] == 'ELECTED MP 2010', mpdata


    electioncontent = root.cssselect('div#electionContent')[0]
    edata = { }
    for dl in root.cssselect('div#electionContent div.gutterUnder dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                edata[key] = dtd
                #print key, lxml.etree.tostring(dtd)
            # re.sub('</?dd[^>]*>', '', lxml.etree.tostring(dtd)).strip()
    assert set(['Sector', 'Votes', 'Detail', 'Majority', 'Position', 'Constituency', "MPs' Expenses"]).issuperset(edata.keys()), edata
    mpdata["employmentsector"] = edata["Sector"].text.strip()
    mpdata["Votes"] = int(edata["Votes"].text.replace(",", ""))
    mpdata["VotePosition"] = int(edata["Position"].text)
    mpdata["Constituency"] = edata["Constituency"][0].text
    mpdata["ConstituencyURL"] = urlparse.urljoin(url, edata["Constituency"][0].attrib.get('href'))
    if "MPs' Expenses" in edata:
        mpdata['expenses'] = edata["MPs' Expenses"][0].attrib.get('href')
    
    odata = { }
    for dl in root.cssselect('div#overview dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                sdtd = lxml.etree.tostring(dtd)
                if re.search('twitter.com', sdtd):
                    odata['twitter'] = dtd
                elif re.search('Facebook group', sdtd):
                    odata['facebook'] = dtd
                else:
                    odata[key] = dtd
                #print key, lxml.etree.tostring(dtd)

    if "Gender" in odata:
        mpdata["gender"] = odata["Gender"].text
    if "Age" in odata:
        mpdata["age"] = int(odata["Age"].text)
    if 'Email' in mpdata:
        mpdata["Email"] = odata["Email"][0].text
    if 'Web' in odata:
        mpdata["webpage"] = odata["Web"][0].attrib.get('href')
    if 'facebook' in odata:
        mpdata["facebook"] = odata["facebook"][0].attrib.get('href')
    if 'twitter' in odata:
        mpdata["twitter"] = odata["twitter"][0].attrib.get('href')

    imagesel = root.cssselect('img.fullCandidateImage')
    if imagesel:
        imagesrc = imagesel[0].attrib.get('src')
        if imagesrc != "http://www.telegraph.co.uk/telegraph/multimedia/archive/01616/silhouette_140_1616987a.jpg":
            mpdata['image'] = imagesrc


    # fill in specific education fields so it is not a list for easier lookup
    for ieducation in mpdata['education']:
        mpdata['education-'+ieducation['level']] = ieducation ['type']

    updateidvals(mpdata)
    scraperwiki.datastore.save(unique_keys=["mpname", "Constituency"], data=mpdata)



def RootLxml(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            if root is not None:
                return root
        except:
            pass
    print "Failed to download", url
    #print urllib.urlopen(url).read()
    return None
        
    


def GetCandidatesForLetter(letter):
    url = "http://ukpolitics.telegraph.co.uk/a-z/candidates/" + letter
    root = RootLxml(url)
    result = [ ]
    atags = root.cssselect('ul.azList li a')
    for i in range(0, len(atags)):
        a = atags[i]
        relativelink = a.attrib.get('href')
        candidatename = a.text
        absolutelink = urlparse.urljoin(url, relativelink)
        result.append((absolutelink, candidatename))
    return result


Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, string

mpnamecorrections = { 'Philip Lee':'Phillip Lee', 'Peter Wishart':'Pete Wishart', 'Robert Neill':'Bob Neill', 
                      'Sir Robert Smith':'Robert Smith', 'Nicholas Brown':'Nick Brown', 'Ed Miliband':'Edward Miliband', 
                      'Edward Garnier QC':'Edward Garnier', 'Huw Irranca Davies':'Huw Irranca-Davies', 
                      'Ian Paisley':'Ian Paisley Jnr', 'Susan Jones':'Susan Elan Jones', 'Sir Menzies Campbell':'Menzies Campbell', 
                      'Sian James':u'Si\xe2n James' }
cnamecorrections = {"Plymouth Sutton & Devonport":"Plymouth, Sutton and Devonport", "Cotswolds, The":"The Cotswolds", 
                    "Plymouth Moor View":"Plymouth, Moor View" }

scraperwiki.sqlite.attach("parlparse")
def updateidvals(mpdata):
    ssql = "* from constituencynames left join constituencies on constituencies.id=constituency_id where text like ?" +\
           " and fromdate <= '2010-05-06' and todate > '2010-05-06' group by constituency_id"
    cname = mpdata["Constituency"].strip()
    cname = cnamecorrections.get(cname, cname)
    result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    if len(result) == 0:
        cname = cname.replace("&", "and")
        result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    assert len(result) == 1, (cname, result)
    mpdata["Constituency_id"] = result[0]["constituency_id"]

    if mpdata.get('status') == 'ELECTED MP 2010':
        mpname = mpdata["mpname"]
        ssql = "* from members where (firstname||' '||lastname) like ? and fromdate = '2010-05-06'"
        mpname = mpnamecorrections.get(mpname, mpname)
        result = scraperwiki.sqlite.select(ssql, mpname, verbose=0)
            # >= date because of Anne McIntosh
        if len(result) == 0:
            ssql = "* from members where lastname like ? and fromdate >= '2010-05-06'"   
            result = scraperwiki.sqlite.select(ssql, mpname.split()[-1], verbose=0)
            if len(result) == 1:
                print "Renaming %s as %s %s" % (mpname, result[0]["firstname"], result[0]["lastname"])
        assert len(result) == 1, (mpname, result)
        mpdata["mp_id"] = result[0]["id"]


def Main():
    #url = "http://ukpolitics.telegraph.co.uk/Bristol+West/Paul+Smith"
    #SingleMPpage(url, "P")
    for letter in "LMNOPQRSTUVWXYZ": # string.ascii_uppercase[16:]:
        candidatesforletter = GetCandidatesForLetter(letter)
        mcandidatesforletter = scraperwiki.sqlite.select("count(*) as c from swdata where letter=?", letter)[0]["c"]
        print "%d candidates on letter: %s, has %d" % (len(candidatesforletter), letter, mcandidatesforletter)
        if mcandidatesforletter == len(candidatesforletter):
            print "skipping"
            continue
        donestart = scraperwiki.sqlite.get_var("done_"+letter, 0)
        print "Starting at: ", donestart
        for i in range(donestart, len(candidatesforletter)):
            curl, name = candidatesforletter[i]
            SingleMPpage(curl, letter)
            scraperwiki.sqlite.save_var("done_"+letter, i, verbose=0)


def SingleMPpage(url, letter):
    root = RootLxml(url)
    if root is None:
        return   # bail out.  lots of data already

    mpdata = { "letter":letter }
    mpdata['mpname'] = root.cssselect('div.headerArea h1')[0].text
    mpdata['url'] = url

    lparty = root.cssselect('div#party p')
    if lparty:
        mpdata['party'] = lparty[0].text.strip(', \t\n')
    else:
        print "Party missing", url

    mpdata['education'] = [ ]
    for table in root.cssselect('table.electionTable'):
        rows = table.cssselect('tr')
        caption = rows[0].cssselect('th div.caption')[0].text
        for row in rows[1:]:
            stype = row[0].text.strip()
            if len(row) == 2:
                sname = row[1].text.strip()
            else:
                sname = stype
                stype = ""
            if sname:
                mpdata['education'].append({'level':caption, 'type':stype, 'name':sname})
    
    lstatus = root.cssselect('div.headerArea div.mpStatus')
    if lstatus:
        mpdata['status'] = lstatus[0].text.strip()
        assert mpdata['status'] == 'ELECTED MP 2010', mpdata


    electioncontent = root.cssselect('div#electionContent')[0]
    edata = { }
    for dl in root.cssselect('div#electionContent div.gutterUnder dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                edata[key] = dtd
                #print key, lxml.etree.tostring(dtd)
            # re.sub('</?dd[^>]*>', '', lxml.etree.tostring(dtd)).strip()
    assert set(['Sector', 'Votes', 'Detail', 'Majority', 'Position', 'Constituency', "MPs' Expenses"]).issuperset(edata.keys()), edata
    mpdata["employmentsector"] = edata["Sector"].text.strip()
    mpdata["Votes"] = int(edata["Votes"].text.replace(",", ""))
    mpdata["VotePosition"] = int(edata["Position"].text)
    mpdata["Constituency"] = edata["Constituency"][0].text
    mpdata["ConstituencyURL"] = urlparse.urljoin(url, edata["Constituency"][0].attrib.get('href'))
    if "MPs' Expenses" in edata:
        mpdata['expenses'] = edata["MPs' Expenses"][0].attrib.get('href')
    
    odata = { }
    for dl in root.cssselect('div#overview dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                sdtd = lxml.etree.tostring(dtd)
                if re.search('twitter.com', sdtd):
                    odata['twitter'] = dtd
                elif re.search('Facebook group', sdtd):
                    odata['facebook'] = dtd
                else:
                    odata[key] = dtd
                #print key, lxml.etree.tostring(dtd)

    if "Gender" in odata:
        mpdata["gender"] = odata["Gender"].text
    if "Age" in odata:
        mpdata["age"] = int(odata["Age"].text)
    if 'Email' in mpdata:
        mpdata["Email"] = odata["Email"][0].text
    if 'Web' in odata:
        mpdata["webpage"] = odata["Web"][0].attrib.get('href')
    if 'facebook' in odata:
        mpdata["facebook"] = odata["facebook"][0].attrib.get('href')
    if 'twitter' in odata:
        mpdata["twitter"] = odata["twitter"][0].attrib.get('href')

    imagesel = root.cssselect('img.fullCandidateImage')
    if imagesel:
        imagesrc = imagesel[0].attrib.get('src')
        if imagesrc != "http://www.telegraph.co.uk/telegraph/multimedia/archive/01616/silhouette_140_1616987a.jpg":
            mpdata['image'] = imagesrc


    # fill in specific education fields so it is not a list for easier lookup
    for ieducation in mpdata['education']:
        mpdata['education-'+ieducation['level']] = ieducation ['type']

    updateidvals(mpdata)
    scraperwiki.datastore.save(unique_keys=["mpname", "Constituency"], data=mpdata)



def RootLxml(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            if root is not None:
                return root
        except:
            pass
    print "Failed to download", url
    #print urllib.urlopen(url).read()
    return None
        
    


def GetCandidatesForLetter(letter):
    url = "http://ukpolitics.telegraph.co.uk/a-z/candidates/" + letter
    root = RootLxml(url)
    result = [ ]
    atags = root.cssselect('ul.azList li a')
    for i in range(0, len(atags)):
        a = atags[i]
        relativelink = a.attrib.get('href')
        candidatename = a.text
        absolutelink = urlparse.urljoin(url, relativelink)
        result.append((absolutelink, candidatename))
    return result


Main()

                        

import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re, string

mpnamecorrections = { 'Philip Lee':'Phillip Lee', 'Peter Wishart':'Pete Wishart', 'Robert Neill':'Bob Neill', 
                      'Sir Robert Smith':'Robert Smith', 'Nicholas Brown':'Nick Brown', 'Ed Miliband':'Edward Miliband', 
                      'Edward Garnier QC':'Edward Garnier', 'Huw Irranca Davies':'Huw Irranca-Davies', 
                      'Ian Paisley':'Ian Paisley Jnr', 'Susan Jones':'Susan Elan Jones', 'Sir Menzies Campbell':'Menzies Campbell', 
                      'Sian James':u'Si\xe2n James' }
cnamecorrections = {"Plymouth Sutton & Devonport":"Plymouth, Sutton and Devonport", "Cotswolds, The":"The Cotswolds", 
                    "Plymouth Moor View":"Plymouth, Moor View" }

scraperwiki.sqlite.attach("parlparse")
def updateidvals(mpdata):
    ssql = "* from constituencynames left join constituencies on constituencies.id=constituency_id where text like ?" +\
           " and fromdate <= '2010-05-06' and todate > '2010-05-06' group by constituency_id"
    cname = mpdata["Constituency"].strip()
    cname = cnamecorrections.get(cname, cname)
    result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    if len(result) == 0:
        cname = cname.replace("&", "and")
        result = scraperwiki.sqlite.select(ssql, cname, verbose=0)
    assert len(result) == 1, (cname, result)
    mpdata["Constituency_id"] = result[0]["constituency_id"]

    if mpdata.get('status') == 'ELECTED MP 2010':
        mpname = mpdata["mpname"]
        ssql = "* from members where (firstname||' '||lastname) like ? and fromdate = '2010-05-06'"
        mpname = mpnamecorrections.get(mpname, mpname)
        result = scraperwiki.sqlite.select(ssql, mpname, verbose=0)
            # >= date because of Anne McIntosh
        if len(result) == 0:
            ssql = "* from members where lastname like ? and fromdate >= '2010-05-06'"   
            result = scraperwiki.sqlite.select(ssql, mpname.split()[-1], verbose=0)
            if len(result) == 1:
                print "Renaming %s as %s %s" % (mpname, result[0]["firstname"], result[0]["lastname"])
        assert len(result) == 1, (mpname, result)
        mpdata["mp_id"] = result[0]["id"]


def Main():
    #url = "http://ukpolitics.telegraph.co.uk/Bristol+West/Paul+Smith"
    #SingleMPpage(url, "P")
    for letter in "LMNOPQRSTUVWXYZ": # string.ascii_uppercase[16:]:
        candidatesforletter = GetCandidatesForLetter(letter)
        mcandidatesforletter = scraperwiki.sqlite.select("count(*) as c from swdata where letter=?", letter)[0]["c"]
        print "%d candidates on letter: %s, has %d" % (len(candidatesforletter), letter, mcandidatesforletter)
        if mcandidatesforletter == len(candidatesforletter):
            print "skipping"
            continue
        donestart = scraperwiki.sqlite.get_var("done_"+letter, 0)
        print "Starting at: ", donestart
        for i in range(donestart, len(candidatesforletter)):
            curl, name = candidatesforletter[i]
            SingleMPpage(curl, letter)
            scraperwiki.sqlite.save_var("done_"+letter, i, verbose=0)


def SingleMPpage(url, letter):
    root = RootLxml(url)
    if root is None:
        return   # bail out.  lots of data already

    mpdata = { "letter":letter }
    mpdata['mpname'] = root.cssselect('div.headerArea h1')[0].text
    mpdata['url'] = url

    lparty = root.cssselect('div#party p')
    if lparty:
        mpdata['party'] = lparty[0].text.strip(', \t\n')
    else:
        print "Party missing", url

    mpdata['education'] = [ ]
    for table in root.cssselect('table.electionTable'):
        rows = table.cssselect('tr')
        caption = rows[0].cssselect('th div.caption')[0].text
        for row in rows[1:]:
            stype = row[0].text.strip()
            if len(row) == 2:
                sname = row[1].text.strip()
            else:
                sname = stype
                stype = ""
            if sname:
                mpdata['education'].append({'level':caption, 'type':stype, 'name':sname})
    
    lstatus = root.cssselect('div.headerArea div.mpStatus')
    if lstatus:
        mpdata['status'] = lstatus[0].text.strip()
        assert mpdata['status'] == 'ELECTED MP 2010', mpdata


    electioncontent = root.cssselect('div#electionContent')[0]
    edata = { }
    for dl in root.cssselect('div#electionContent div.gutterUnder dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                edata[key] = dtd
                #print key, lxml.etree.tostring(dtd)
            # re.sub('</?dd[^>]*>', '', lxml.etree.tostring(dtd)).strip()
    assert set(['Sector', 'Votes', 'Detail', 'Majority', 'Position', 'Constituency', "MPs' Expenses"]).issuperset(edata.keys()), edata
    mpdata["employmentsector"] = edata["Sector"].text.strip()
    mpdata["Votes"] = int(edata["Votes"].text.replace(",", ""))
    mpdata["VotePosition"] = int(edata["Position"].text)
    mpdata["Constituency"] = edata["Constituency"][0].text
    mpdata["ConstituencyURL"] = urlparse.urljoin(url, edata["Constituency"][0].attrib.get('href'))
    if "MPs' Expenses" in edata:
        mpdata['expenses'] = edata["MPs' Expenses"][0].attrib.get('href')
    
    odata = { }
    for dl in root.cssselect('div#overview dl'):
        key = None
        for dtd in dl:
            if dtd.tag == 'dt':
                key = dtd.text.strip(': \t\n')
            if dtd.tag == 'dd':
                sdtd = lxml.etree.tostring(dtd)
                if re.search('twitter.com', sdtd):
                    odata['twitter'] = dtd
                elif re.search('Facebook group', sdtd):
                    odata['facebook'] = dtd
                else:
                    odata[key] = dtd
                #print key, lxml.etree.tostring(dtd)

    if "Gender" in odata:
        mpdata["gender"] = odata["Gender"].text
    if "Age" in odata:
        mpdata["age"] = int(odata["Age"].text)
    if 'Email' in mpdata:
        mpdata["Email"] = odata["Email"][0].text
    if 'Web' in odata:
        mpdata["webpage"] = odata["Web"][0].attrib.get('href')
    if 'facebook' in odata:
        mpdata["facebook"] = odata["facebook"][0].attrib.get('href')
    if 'twitter' in odata:
        mpdata["twitter"] = odata["twitter"][0].attrib.get('href')

    imagesel = root.cssselect('img.fullCandidateImage')
    if imagesel:
        imagesrc = imagesel[0].attrib.get('src')
        if imagesrc != "http://www.telegraph.co.uk/telegraph/multimedia/archive/01616/silhouette_140_1616987a.jpg":
            mpdata['image'] = imagesrc


    # fill in specific education fields so it is not a list for easier lookup
    for ieducation in mpdata['education']:
        mpdata['education-'+ieducation['level']] = ieducation ['type']

    updateidvals(mpdata)
    scraperwiki.datastore.save(unique_keys=["mpname", "Constituency"], data=mpdata)



def RootLxml(url):
    for i in range(3):
        try:
            root = lxml.html.parse(url).getroot()
            if root is not None:
                return root
        except:
            pass
    print "Failed to download", url
    #print urllib.urlopen(url).read()
    return None
        
    


def GetCandidatesForLetter(letter):
    url = "http://ukpolitics.telegraph.co.uk/a-z/candidates/" + letter
    root = RootLxml(url)
    result = [ ]
    atags = root.cssselect('ul.azList li a')
    for i in range(0, len(atags)):
        a = atags[i]
        relativelink = a.attrib.get('href')
        candidatename = a.text
        absolutelink = urlparse.urljoin(url, relativelink)
        result.append((absolutelink, candidatename))
    return result


Main()

                        

