import scraperwiki
import mechanize
import re
import urlparse
import lxml.html


# ASPX pages are some of the hardest challenges because they use javascript and forms to navigate
# Almost always the links go through the function function __doPostBack(eventTarget, eventArgument)
# which you have to simulate in the mechanize form handling library

# This example shows how to follow the Next page link

url = 'http://www.totaljobs.com/JobSearch/Results.aspx?Keywords=&Sort=0&LTxt=Halton%2c+Runcorn&Radius=5'
url2 = 'http://www.reed.co.uk/job/searchresults.aspx?k=&jto=false&s=&l=Halton%2C+Cheshire&lp=5&ms=From&mxs=To&st=5&ns=true&da=8630'
url3 = 'http://jobsearch.monster.co.uk/jobs/North-West+Cheshire-_12?lv=Entry-Level&where=WA72AB__2c-Runcorn__2c-North-West&rad=2-mi&sort=di.rv.dt&cy=uk'
br = mechanize.Browser()
br2 = mechanize.Browser()
br3 = mechanize.Browser()

    # sometimes the server is sensitive to this information
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br2.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br3.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
response2 = br2.open(url2)
response3 = br3.open(url3)


html3 = response3.read()
re.DOTALL
jobtitlemonster = re.findall('class="jobTitle fnt11_js"(.*?)</a>', html3)
locationmonster = re.findall('<span class="jobplace">.*?>(.*?)</a>', html3)
companymonster = re.findall('<span class="company">(.*?)</span>',html3)
print jobtitlemonster
print locationmonster
print companymonster

allattsmonster = jobtitlemonster, locationmonster, companymonster
attssortmonsters = [[row[i] for row in allattsmonster] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]






html2 = response2.read()
re.DOTALL
print "NEW TEST", re.findall("h4>(.*?)</a>", html2)
jobtitlereeds = re.findall("h4>(.*?)</a>", html2)
locationreed = re.findall("Location</label>(.*?)</div>",html2)
salaryreed = re.findall("Salary</label>(.*?)</div>",html2)
companyreed = re.findall("Recruiter</label>(.*?)</div>",html2)
print "OOOOOOOOOOOOOOO", jobtitlereeds
allattsreed = jobtitlereeds, locationreed, salaryreed, companyreed

attssortreeds = [[row[i] for row in allattsreed] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]



for pagenum in range(10):
    html = response.read()
    print "Page %d  page length %d" % (pagenum, len(html))
    re.DOTALL
    print "Jobs found:", re.findall("rptSearchResults_ctl.*?lnkJobTitle.*?>(.*?)</a>", html)
    print "salarys found:", re.findall("dd>(.*?)</dd>", html)
    print "Jobs found:", re.findall("h2>(.*?)</a>", html)
    jobs = re.findall("h2>(.*?)</a>", html)
    print jobs
    salarys = re.findall("dd>(.*?)</dd>", html)
    pays = salarys.pop(1), salarys.pop(5), salarys.pop(9), salarys.pop(13), salarys.pop(17), salarys.pop(21), salarys.pop(25), salarys.pop(29), salarys.pop(33), salarys.pop(37), salarys.pop(41), salarys.pop(45), salarys.pop(49), salarys.pop(53), salarys.pop(57), salarys.pop(61), salarys.pop(65), salarys.pop(69), salarys.pop(73), salarys.pop(77)
    locat = salarys.pop(0), salarys.pop(3), salarys.pop(6), salarys.pop(9), salarys.pop(12), salarys.pop(15), salarys.pop(18), salarys.pop(21), salarys.pop(24), salarys.pop(27), salarys.pop(30), salarys.pop(33), salarys.pop(36), salarys.pop(39), salarys.pop(42), salarys.pop(45), salarys.pop(48), salarys.pop(51), salarys.pop(54), salarys.pop(57)
    permortemp = salarys.pop(1), salarys.pop(3), salarys.pop(5), salarys.pop(7), salarys.pop(9), salarys.pop(11), salarys.pop(13), salarys.pop(15), salarys.pop(17), salarys.pop(19), salarys.pop(21), salarys.pop(23), salarys.pop(25), salarys.pop(27), salarys.pop(29), salarys.pop(31), salarys.pop(33), salarys.pop(35), salarys.pop(37), salarys.pop(39)
    company = salarys.pop(1), salarys.pop(2), salarys.pop(3), salarys.pop(4), salarys.pop(5), salarys.pop(6), salarys.pop(7), salarys.pop(8), salarys.pop(9), salarys.pop(10), salarys.pop(11), salarys.pop(12), salarys.pop(13), salarys.pop(14), salarys.pop(15), salarys.pop(16), salarys.pop(17), salarys.pop(18), salarys.pop(19), salarys.pop(20)


    print "Locations: ", locat
    print "Types: ", permortemp
    print "Other: ", company
    
    allatts = jobs, pays, locat, permortemp, company

    attsends = [[row[i] for row in allatts] for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]]

    print "all attributes: ", allatts
    print "all records: ", attsends

    mnextlink = re.search("javascript:WebForm_DoPostBackWithOptions(new  WebForm_PostBackOptions(&quot;srpPager$btnForward&quot;,  &quot;&quot;,  true, &quot;&quot;, &quot;&quot;,  false, true))", html)
    if not mnextlink:
        break

    br.select_form(name='frmMain')
    br.form.set_all_readonly(False)
    br['__EVENTTARGET'] = 'srpPager_btnForward'
    br['__EVENTARGUMENT'] = ''
    response = br.submit()

scraperwiki.sqlite.execute("delete from swdata") 

record = {}
for attsend in attsends:
    if jobs:
        record['Job'] = attsend[0]
        record['Salary'] = attsend[1]
        record['Location'] = attsend[2]
        record['Type'] = attsend[3]
        record['Company'] = attsend[4]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Job"], record)

for attssortreed in attssortreeds:
    if jobtitlereeds:
        record['Job'] = attssortreed[0]
        record['Salary'] = attssortreed[2]
        record['Location'] = attssortreed[1]
        record['Type'] = "N/A"
        record['Company'] = attssortreed[3]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Job"], record)

for attssortmonster in attssortmonsters:
    if jobtitlemonster:
        record['Job'] = attssortmonster[0]
        record['Salary'] = "N/A"
        record['Location'] = attssortmonster[1]
        record['Type'] = "N/A"
        record['Company'] = attssortmonster[2]

        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Artist' is our unique key
        scraperwiki.sqlite.save(["Job"], record)
