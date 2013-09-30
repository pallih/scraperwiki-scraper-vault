import scraperwiki
import lxml.html
import re

def firstorblank(elemList):
    if ( elemList == None or len(elemList) < 1):
        return ''
    else:
        return elemList[0].text_content()


baseurl = 'http://www.kath.ch/index.php?&na=22,0,0,0,d&initial='

for letter in map(chr, range(65, 91)):
#for letter in [ 'L' ]:
    print "%s%s" % (baseurl, letter)
    html = scraperwiki.scrape( "%s%s" % (baseurl, letter) )
    root = lxml.html.fromstring(html)
    root.make_links_absolute(baseurl)
    links = root.cssselect('div.halfL ul li a')
    if len(links) > 0:
        for link in links:
            m = re.search('.*,(\d+)', link.attrib['href'])
            if m:
                label = m.group(1)
            else:
                label = ''
            print "Using label %s" % label
            locpage = scraperwiki.scrape( link.attrib['href'] )
            locroot = lxml.html.fromstring(locpage)
            name = firstorblank(locroot.cssselect('div.halfL h2'))
            if (name == ''):
                continue
            addrlines = locroot.xpath('//div[@class="halfL"]/p/text()')
            addr = []
            for line in addrlines:
                addr.append(line)

            phoneElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "T"]/td[2]')
            faxElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "F"]/td[2]')
            emailElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "E"]/td[2]')
            webElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "W"]/td[2]')
            
            phone = firstorblank(phoneElem)
            fax = firstorblank(faxElem)
            email = firstorblank(emailElem)
            website = firstorblank(webElem)

            data = {
                'label' : "%s" % label,
                'name' : name,
                'address' : addr,
                'phone' : phone,
                'fax' : fax,
                'email' : email,
                'website' : website
            }

            orgdetails = locroot.xpath('//div[@class="halfR"]/table[1]/tr')
            for row in orgdetails:
                label = "%s" % row.xpath('.//td[1]')[0].text_content().encode('utf-8').decode('ascii', 'ignore')
                m = re.search('(\w+).*', label)
                if m:
                    label = m.group(1).lower()
                else:
                    continue
                value = row.xpath('.//td[2]')[0].text_content()
                #print "Setting %s = %s" % (label, value)
                data[label] = value
            peopledetails = locroot.xpath('//div[@class="halfR"]/table[2]/tr')
            for row in peopledetails:
                label = "%s" % row.xpath('.//td[1]')[0].text_content().encode('utf-8').decode('ascii', 'ignore')
                m = re.search('(\w+).*', label)
                if m:
                    label = m.group(1).lower()
                else:
                    continue
                value = row.xpath('.//td[2]')[0].text_content()
                #print "Setting %s = %s" % (label, value)
                vallist = data.setdefault(label, [])
                vallist.append(value)
                data[label] = vallist
                
            scraperwiki.sqlite.save(unique_keys=['label'], data=data)

import scraperwiki
import lxml.html
import re

def firstorblank(elemList):
    if ( elemList == None or len(elemList) < 1):
        return ''
    else:
        return elemList[0].text_content()


baseurl = 'http://www.kath.ch/index.php?&na=22,0,0,0,d&initial='

for letter in map(chr, range(65, 91)):
#for letter in [ 'L' ]:
    print "%s%s" % (baseurl, letter)
    html = scraperwiki.scrape( "%s%s" % (baseurl, letter) )
    root = lxml.html.fromstring(html)
    root.make_links_absolute(baseurl)
    links = root.cssselect('div.halfL ul li a')
    if len(links) > 0:
        for link in links:
            m = re.search('.*,(\d+)', link.attrib['href'])
            if m:
                label = m.group(1)
            else:
                label = ''
            print "Using label %s" % label
            locpage = scraperwiki.scrape( link.attrib['href'] )
            locroot = lxml.html.fromstring(locpage)
            name = firstorblank(locroot.cssselect('div.halfL h2'))
            if (name == ''):
                continue
            addrlines = locroot.xpath('//div[@class="halfL"]/p/text()')
            addr = []
            for line in addrlines:
                addr.append(line)

            phoneElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "T"]/td[2]')
            faxElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "F"]/td[2]')
            emailElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "E"]/td[2]')
            webElem = locroot.xpath('//div[@class="halfL"]/table/tr[td[1] = "W"]/td[2]')
            
            phone = firstorblank(phoneElem)
            fax = firstorblank(faxElem)
            email = firstorblank(emailElem)
            website = firstorblank(webElem)

            data = {
                'label' : "%s" % label,
                'name' : name,
                'address' : addr,
                'phone' : phone,
                'fax' : fax,
                'email' : email,
                'website' : website
            }

            orgdetails = locroot.xpath('//div[@class="halfR"]/table[1]/tr')
            for row in orgdetails:
                label = "%s" % row.xpath('.//td[1]')[0].text_content().encode('utf-8').decode('ascii', 'ignore')
                m = re.search('(\w+).*', label)
                if m:
                    label = m.group(1).lower()
                else:
                    continue
                value = row.xpath('.//td[2]')[0].text_content()
                #print "Setting %s = %s" % (label, value)
                data[label] = value
            peopledetails = locroot.xpath('//div[@class="halfR"]/table[2]/tr')
            for row in peopledetails:
                label = "%s" % row.xpath('.//td[1]')[0].text_content().encode('utf-8').decode('ascii', 'ignore')
                m = re.search('(\w+).*', label)
                if m:
                    label = m.group(1).lower()
                else:
                    continue
                value = row.xpath('.//td[2]')[0].text_content()
                #print "Setting %s = %s" % (label, value)
                vallist = data.setdefault(label, [])
                vallist.append(value)
                data[label] = vallist
                
            scraperwiki.sqlite.save(unique_keys=['label'], data=data)

