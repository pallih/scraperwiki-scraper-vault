import scraperwiki
import re

# Blank Python

html = scraperwiki.scrape('http://www.utexas.edu/world/comcol/state/')
print html

schools = re.findall(r'"(http://(?:www)?\.[\w\.]+\edu/).*?"', html)
schools = list(set(schools))

print schools
import scraperwiki
import re

# Blank Python

html = scraperwiki.scrape('http://www.utexas.edu/world/comcol/state/')
print html

schools = re.findall(r'"(http://(?:www)?\.[\w\.]+\edu/).*?"', html)
schools = list(set(schools))

print schools
