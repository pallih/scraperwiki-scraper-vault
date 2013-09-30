# David Jones, Climate Code Foundation
import re
import urllib

# Converts &amp; to &, and so on.
from xml.sax.saxutils import unescape

import scraperwiki

page = "http://www.sheffield.gov.uk/education/our-schools/find-a-school/XXX"
# Currently in the UK, for these purposes, there are primary schools (includes infants),
# secondary schools (includes 6th form), and Special schools (Special Education Needs: SEN).
schooltypes = "primary secondary sen".split()

def urls():
    """Generate a sequence of (schooltype,URL) pairs."""
    for t in schooltypes:
        url = page.replace('XXX', t)
        yield t,url


for schooltype,url in urls():
    for line in urllib.urlopen(url):
        matches = [x for x in re.findall(r'src.*?=.*?"(.*?)"', line) if 'output=embed' in x]
        if matches:
            assert len(matches) == 1
            target, = matches
            print schooltype,target
            target = target.replace('output=embed', 'output=kml')
            if '&amp' in target:
                # The SEN page has incorrectly escaped (that is, not) URLs in its HTML.
                target = unescape(target)
            print target
            scraperwiki.sqlite.save(['area', 'type'], dict(area='sheffield', type=schooltype, url=target))
# David Jones, Climate Code Foundation
import re
import urllib

# Converts &amp; to &, and so on.
from xml.sax.saxutils import unescape

import scraperwiki

page = "http://www.sheffield.gov.uk/education/our-schools/find-a-school/XXX"
# Currently in the UK, for these purposes, there are primary schools (includes infants),
# secondary schools (includes 6th form), and Special schools (Special Education Needs: SEN).
schooltypes = "primary secondary sen".split()

def urls():
    """Generate a sequence of (schooltype,URL) pairs."""
    for t in schooltypes:
        url = page.replace('XXX', t)
        yield t,url


for schooltype,url in urls():
    for line in urllib.urlopen(url):
        matches = [x for x in re.findall(r'src.*?=.*?"(.*?)"', line) if 'output=embed' in x]
        if matches:
            assert len(matches) == 1
            target, = matches
            print schooltype,target
            target = target.replace('output=embed', 'output=kml')
            if '&amp' in target:
                # The SEN page has incorrectly escaped (that is, not) URLs in its HTML.
                target = unescape(target)
            print target
            scraperwiki.sqlite.save(['area', 'type'], dict(area='sheffield', type=schooltype, url=target))
