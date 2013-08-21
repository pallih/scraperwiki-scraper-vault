import urllib
import scraperwiki
import re
import datetime


def ProcessRow(row):
    assert len(row) == 4, row
    assert row[1] == '\xc2\xa3'
    data = { }
    data["amount"] = float(re.sub(",", "", row[0]))
    data["vendor"] = row[2]
    ldate, docnum = row[3].split()
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', ldate)
    data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    data["docnum"] = docnum
    scraperwiki.datastore.save(unique_keys = ["docnum"], data = data, date = data["date"])
    
    #['1,000.00', '\xc2\xa3 ', '3D EDUCATION CONSULTANCY LTD', '16/08/2010 3144213353']


def Main():
    x = GetPDFtrans2()
    y = re.findall('<text top="(\d+)" left="(\d+)".*?>(.*?)</text>', x)
    lasttop = ""
    allrows = [ ]

    for v in y:
        if v[0] != lasttop:
            if len(allrows) >= 2:
                ProcessRow(allrows[-1])
            allrows.append([])
            lasttop = v[0]
        allrows[-1].append(v[2].strip())
        


def GetPDFtrans():
    pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+%C2%A3500+August.pdf"
    c = urllib.urlopen(pdfurl).read()
    x = scraperwiki.pdftoxml(c)
    print x[:4000]
    urlup = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi"
    d = urllib.urlencode({"name":"brumpdf500xml", "contents":x})
    print urllib.urlopen(urlup, d).read()


def GetPDFtrans2():
    return urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/brumpdf500xml").read()





Main()

import urllib
import scraperwiki
import re
import datetime


def ProcessRow(row):
    assert len(row) == 4, row
    assert row[1] == '\xc2\xa3'
    data = { }
    data["amount"] = float(re.sub(",", "", row[0]))
    data["vendor"] = row[2]
    ldate, docnum = row[3].split()
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', ldate)
    data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    data["docnum"] = docnum
    scraperwiki.datastore.save(unique_keys = ["docnum"], data = data, date = data["date"])
    
    #['1,000.00', '\xc2\xa3 ', '3D EDUCATION CONSULTANCY LTD', '16/08/2010 3144213353']


def Main():
    x = GetPDFtrans2()
    y = re.findall('<text top="(\d+)" left="(\d+)".*?>(.*?)</text>', x)
    lasttop = ""
    allrows = [ ]

    for v in y:
        if v[0] != lasttop:
            if len(allrows) >= 2:
                ProcessRow(allrows[-1])
            allrows.append([])
            lasttop = v[0]
        allrows[-1].append(v[2].strip())
        


def GetPDFtrans():
    pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+%C2%A3500+August.pdf"
    c = urllib.urlopen(pdfurl).read()
    x = scraperwiki.pdftoxml(c)
    print x[:4000]
    urlup = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi"
    d = urllib.urlencode({"name":"brumpdf500xml", "contents":x})
    print urllib.urlopen(urlup, d).read()


def GetPDFtrans2():
    return urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/brumpdf500xml").read()





Main()

import urllib
import scraperwiki
import re
import datetime


def ProcessRow(row):
    assert len(row) == 4, row
    assert row[1] == '\xc2\xa3'
    data = { }
    data["amount"] = float(re.sub(",", "", row[0]))
    data["vendor"] = row[2]
    ldate, docnum = row[3].split()
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', ldate)
    data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    data["docnum"] = docnum
    scraperwiki.datastore.save(unique_keys = ["docnum"], data = data, date = data["date"])
    
    #['1,000.00', '\xc2\xa3 ', '3D EDUCATION CONSULTANCY LTD', '16/08/2010 3144213353']


def Main():
    x = GetPDFtrans2()
    y = re.findall('<text top="(\d+)" left="(\d+)".*?>(.*?)</text>', x)
    lasttop = ""
    allrows = [ ]

    for v in y:
        if v[0] != lasttop:
            if len(allrows) >= 2:
                ProcessRow(allrows[-1])
            allrows.append([])
            lasttop = v[0]
        allrows[-1].append(v[2].strip())
        


def GetPDFtrans():
    pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+%C2%A3500+August.pdf"
    c = urllib.urlopen(pdfurl).read()
    x = scraperwiki.pdftoxml(c)
    print x[:4000]
    urlup = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi"
    d = urllib.urlencode({"name":"brumpdf500xml", "contents":x})
    print urllib.urlopen(urlup, d).read()


def GetPDFtrans2():
    return urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/brumpdf500xml").read()





Main()

import urllib
import scraperwiki
import re
import datetime


def ProcessRow(row):
    assert len(row) == 4, row
    assert row[1] == '\xc2\xa3'
    data = { }
    data["amount"] = float(re.sub(",", "", row[0]))
    data["vendor"] = row[2]
    ldate, docnum = row[3].split()
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', ldate)
    data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    data["docnum"] = docnum
    scraperwiki.datastore.save(unique_keys = ["docnum"], data = data, date = data["date"])
    
    #['1,000.00', '\xc2\xa3 ', '3D EDUCATION CONSULTANCY LTD', '16/08/2010 3144213353']


def Main():
    x = GetPDFtrans2()
    y = re.findall('<text top="(\d+)" left="(\d+)".*?>(.*?)</text>', x)
    lasttop = ""
    allrows = [ ]

    for v in y:
        if v[0] != lasttop:
            if len(allrows) >= 2:
                ProcessRow(allrows[-1])
            allrows.append([])
            lasttop = v[0]
        allrows[-1].append(v[2].strip())
        


def GetPDFtrans():
    pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+%C2%A3500+August.pdf"
    c = urllib.urlopen(pdfurl).read()
    x = scraperwiki.pdftoxml(c)
    print x[:4000]
    urlup = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi"
    d = urllib.urlencode({"name":"brumpdf500xml", "contents":x})
    print urllib.urlopen(urlup, d).read()


def GetPDFtrans2():
    return urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/brumpdf500xml").read()





Main()

import urllib
import scraperwiki
import re
import datetime


def ProcessRow(row):
    assert len(row) == 4, row
    assert row[1] == '\xc2\xa3'
    data = { }
    data["amount"] = float(re.sub(",", "", row[0]))
    data["vendor"] = row[2]
    ldate, docnum = row[3].split()
    mdate = re.match('(\d\d)/(\d\d)/(\d\d\d\d)$', ldate)
    data["date"] = datetime.date(int(mdate.group(3)), int(mdate.group(2)), int(mdate.group(1)))
    data["docnum"] = docnum
    scraperwiki.datastore.save(unique_keys = ["docnum"], data = data, date = data["date"])
    
    #['1,000.00', '\xc2\xa3 ', '3D EDUCATION CONSULTANCY LTD', '16/08/2010 3144213353']


def Main():
    x = GetPDFtrans2()
    y = re.findall('<text top="(\d+)" left="(\d+)".*?>(.*?)</text>', x)
    lasttop = ""
    allrows = [ ]

    for v in y:
        if v[0] != lasttop:
            if len(allrows) >= 2:
                ProcessRow(allrows[-1])
            allrows.append([])
            lasttop = v[0]
        allrows[-1].append(v[2].strip())
        


def GetPDFtrans():
    pdfurl = "http://www.birmingham.gov.uk/cs/Satellite?%26ssbinary=true&blobcol=urldata&blobheader=application%2Fpdf&blobheadername1=Content-Disposition&blobkey=id&blobtable=MungoBlobs&blobwhere=1223439077563&blobheadervalue1=attachment%3B+filename%3D444523Payments+over+%C2%A3500+August.pdf"
    c = urllib.urlopen(pdfurl).read()
    x = scraperwiki.pdftoxml(c)
    print x[:4000]
    urlup = "http://seagrass.goatchurch.org.uk/~julian/cgi-bin/uu.cgi"
    d = urllib.urlencode({"name":"brumpdf500xml", "contents":x})
    print urllib.urlopen(urlup, d).read()


def GetPDFtrans2():
    return urllib.urlopen("http://seagrass.goatchurch.org.uk/~julian/uusaves/brumpdf500xml").read()





Main()

