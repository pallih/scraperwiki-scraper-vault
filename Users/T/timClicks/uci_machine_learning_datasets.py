import lxml

import scraperwiki
import scrapemark

url = "http://archive.ics.uci.edu/ml/datasets.html"


print scrapemark.scrape(pattern='{ <p class="normal"><b><a>{{ title }}</a></b></p> }}', url=url)
