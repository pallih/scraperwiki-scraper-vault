import scraperwiki
import re
import time
import sys


# Blank Python



reCVE = "<a .*?>(\\d+-\\d+)</a>"
reOSVBD ="<a .*?>(\\d+)</a>"


regex='(?:EDB-ID:\\s+<span class="r1">)(\\d+)<\\/span>'
regex+='.*?(?:CVE:\\s+(.*?)</td>)'
regex+='.*?(?:OSVDB-ID:\\s+(.*?)</td>)'
regex+='.*?(?:>Author:\\s+(.*?)<)'
regex+='.*?(?:>Published:\\s+(.*?)<)'
regex+='.*?(?:>Verified:\\s+(.*?)</td>)'   

print regex


rg = re.compile(regex,re.IGNORECASE|re.DOTALL)
rg1  = re.compile(reCVE, re.IGNORECASE)
rg2  = re.compile(reOSVBD, re.IGNORECASE)
errors = ""

for i in range(1,25001):
    try:
        html = scraperwiki.scrape("http://www.exploit-db.com/exploits/"+str(i)+"/")
        m = rg.search(html)
        
        if m:
            if int(m.group(1)) !=  i:
                error= str(i) + ": EDB-ID not matched: " + m.group(1)
                #errdata = { "index":str(i), "error":error }
                #scraperwiki.sqlite.save(data=errdata)
                errors += error + "\n"
                print "§KH$ERROR: " + error
                continue
            m1= rg1.search(m.group(2))
            if m1:
                cveId = m1.group(1)
            else:
                cveId = 'N/A'

            m2= rg2.search(m.group(3))
            if m1:
                osvbdId = m2.group(1)
            else:
                osvbdId = 'N/A'
            
            if 'accept' in m.group(6):
                verf = "True"
            else:
                verf = "False"
            data = {
                'EDB-ID' : m.group(1),
                'CVE' : cveId,
                'OSVBD-ID' : osvbdId,
                'Author' : m.group(4),
                'Published' :m.group(5),
                'Verified' : verf}
            scraperwiki.sqlite.save(unique_keys=['EDB-ID'], data=data)
        else:
            error= str(i) + ": regex not matched\n"
            #errdata = { "index":str(i), "error":error }
            #scraperwiki.sqlite.save(data=errdata)
            errors += error + "\n"
            print "§KH$ERROR: " + error
    except Exception as e:
        error= str(i) + "Unexpected error:" + str(e) + "\n"
        #errdata = { "index":str(i), "error":error }
        #scraperwiki.sqlite.save(unique_keys=['error'],data=errdata)
        errors += error + "\n"
        print "§KH$ERROR: " + error
        continue
    

print errors
