import scraperwiki
import re

page = scraperwiki.scrape("http://osc.hul.harvard.edu/dash/mydash")
result = re.search('\["alldash","All","(\d+)","(\d+)","(\d+)"', page)
total = int(result.group(3))

print total
import scraperwiki
import re

page = scraperwiki.scrape("http://osc.hul.harvard.edu/dash/mydash")
result = re.search('\["alldash","All","(\d+)","(\d+)","(\d+)"', page)
total = int(result.group(3))

print total
