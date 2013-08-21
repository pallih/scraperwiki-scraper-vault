import scraperwiki
import urllib2
import datetime
import lxml.html
import re
import time

jobDes = set (['Experienced Farm Worker', 'Counter Assistant', 'Cleaner', 'Cleaning Operative', 'Experienced Cleaners', 'Part-time Cleaner', 'General Assistant', 'Valet / Driver', 'Labourer', 'Experienced Handyman', 'Taxi Driver', 'Taxi Drivers', 'Admin Officer - Enforcement', 'Kitchen Assistant', 'Kitchen Porter'])

def br2text(el):
    res = [el.text]
    for br in el:
#        print res
        assert br.tag == 'br'
        if br.tail != None:
            res.append(br.tail)
#    print res
    return ", ".join(res)
#
def mmdates(jdate):
    if not jdate:
        return None
#    print "jdate", jdate
    edate = re.match("(\d{1,2}?)\s(\w\w\w)\s(\d\d\d\d)$", jdate)

    monthtext = str(edate.group(2))
#    print monthtext
#    print str(edate.group(1))
#    print str(edate.group(2))
#    print str(edate.group(3))
# use strptime(string, format_str) to form a time tuple
# (year,month,day,hour,min,sec,weekday(Monday=0),yearday,dls-flag)
    time_tuple = time.strptime(monthtext, "%b") 
# use time.strftime(format_str, time_tuple) to create new format
    monthnum = time.strftime("%m", time_tuple) 
#    print "monthtext", monthtext
#    print "monthnum", monthnum
    return datetime.date(int(edate.group(3)), int(monthnum), int(edate.group(1)))

def pdata(number, html): 
    root = lxml.html.fromstring(html)
    tables = root.cssselect("table.searchResults")
    regNo = "%05d" % (number)

    for table in tables:
        rows = table.cssselect("tr")
#        print rows
        th = rows[0].cssselect("th")
        assert 1 <= len(th) <= 2, html
        if len(th[0]) == 1:
            title = th[0][0].text.strip()
        else:
            title = th[0].text.strip()
#       assert title in jobDes, html
#        print "title", title
        data = { }
        for row in rows[0:]:
            assert (len(row) == 2 and row[0].tag == "th" and row[1].tag == "td"), lxml.html.tostring(row)
            
            key = re.sub("[ :.-]", "", row[0].text.strip())
#            print "key", key
            assert key in ['ReferenceID', 'Job', 'Firm', 'Address', 'Contact', 'TelNo', 'NumberRequired', 'Hours', 'Duration', 'Salary', 'EndDate', 'Notes', 'PostCode'], (key, title)
            
#            print "data", data
#            print "row0"
#            print lxml.html.tostring(row[0])
#            print "row1"
#            print lxml.html.tostring(row[1])



            if lxml.html.tostring(row[1]) != '<td></td>':
#                print '@',lxml.html.tostring(row[1]),'@'
                val = br2text(row[1]).strip()
            else:
                val = "N/A"
            
#            val = row[1].strip().replace('<br>', '')  

#  ([a-zA-Z]{2}[0-9]{1,2}\s{0,monthtext = str(edate.group(2)1}[0-9]{1,2}[a-zA-Z]{2})
            if val:
#                print "key7", key[:7]
                if key[:7] == "Address":
#                    print lxml.html.tostring(row[1])
                    postcodesource = lxml.html.tostring(row[1])
#                    print postcodesource
#([a-zA-Z]{1,2}[1-9][0-9]?\s?[0-9][0-9]?[a-zA-Z]{1,2})
                    postcode = re.search("([a-zA-Z]{1,2}[1-9][0-9]?\s?[0-9][0-9]?[a-zA-Z]{1,2})", postcodesource)
                    if postcode != None:
                        postcodetext = str(postcode.group(0))
                        print "postcode1", postcodetext
                    else:
                        postcodetext = "N/A"
                        print "postcode2: ", postcodetext  
                  
            if val:
#                print "key10", key[:7]
#                print "1", val
                if key[:7] == "EndDate":
                    val = mmdates(val)
#                    print "2", val
                data[key] = val
#            print regNo
#            print data
#            print data[key]
            
            assert data["ReferenceID"] == regNo, data
        
        scraperwiki.sqlite.save(unique_keys=["ReferenceID"], data=data)
        print "data saved"
def Mainp():
    rows = scraperwiki.sqlite.attach("playing_w_python", "pwp")
    rows = scraperwiki.sqlite.select("number, html from pwp.draft")
    for row in rows:
        pdata(row["number"], row["html"])
    

Mainp()