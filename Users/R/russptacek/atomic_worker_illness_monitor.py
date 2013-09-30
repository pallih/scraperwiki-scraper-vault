import scraperwiki
import urllib
import re

# should make a loop over the a different list of webpages which we are all monitoring

urlc = [('http://www.dol.gov/owcp/energy/regs/compliance/statistics/WebPages/KANSAS_PLANT.htm', '(?s)KANSAS CITY PLANT.*Final Decision'), 
  ('http://www.gsaig.gov/index.cfm/oig-reports/audit-reports/fy-2012-audit-reports-october-1-2011-to-september-30-2012/', '')
]


url, mat = urlc[0]

x = urllib.urlopen(url).read()
s = re.search(mat, x)
sc = s.group(0)

previous_sc = scraperwiki.sqlite.get_var('previous_sc', '')
if sc != previous_sc:
    print "EMAILSUBJECT: Check out new thing at Bannister"
    print "There's been a new update at\n\n", url

    scraperwiki.sqlite.save_var('previous_sc', sc)import scraperwiki
import urllib
import re

# should make a loop over the a different list of webpages which we are all monitoring

urlc = [('http://www.dol.gov/owcp/energy/regs/compliance/statistics/WebPages/KANSAS_PLANT.htm', '(?s)KANSAS CITY PLANT.*Final Decision'), 
  ('http://www.gsaig.gov/index.cfm/oig-reports/audit-reports/fy-2012-audit-reports-october-1-2011-to-september-30-2012/', '')
]


url, mat = urlc[0]

x = urllib.urlopen(url).read()
s = re.search(mat, x)
sc = s.group(0)

previous_sc = scraperwiki.sqlite.get_var('previous_sc', '')
if sc != previous_sc:
    print "EMAILSUBJECT: Check out new thing at Bannister"
    print "There's been a new update at\n\n", url

    scraperwiki.sqlite.save_var('previous_sc', sc)