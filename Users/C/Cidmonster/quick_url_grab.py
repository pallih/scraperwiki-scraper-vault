import scraperwiki
import re
import urllib

# Blank Python

def Main():
    school = ' '
    html = urllib.urlopen('http://www.utexas.edu/world/comcol/state/').read()
    for match in re.finditer('www\.([\w\.]+\.edu)', html):
          domain = match.group(1)
          record = {}
          record['school'] = domain
          scraperwiki.sqlite.save(['school'], record)
          record = {}    

Main()
import scraperwiki
import re
import urllib

# Blank Python

def Main():
    school = ' '
    html = urllib.urlopen('http://www.utexas.edu/world/comcol/state/').read()
    for match in re.finditer('www\.([\w\.]+\.edu)', html):
          domain = match.group(1)
          record = {}
          record['school'] = domain
          scraperwiki.sqlite.save(['school'], record)
          record = {}    

Main()
