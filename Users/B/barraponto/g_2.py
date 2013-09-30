import scraperwiki
from lxml.html import parse

source = 'https://ahpn.lib.utexas.edu/search/'

doc = parse(source).getroot()

# word

doc.make_absolute_urls()import scraperwiki
from lxml.html import parse

source = 'https://ahpn.lib.utexas.edu/search/'

doc = parse(source).getroot()

# word

doc.make_absolute_urls()