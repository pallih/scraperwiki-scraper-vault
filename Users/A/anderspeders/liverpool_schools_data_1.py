# Liverpool Schools Data

# Data from Dept for Education (released under Crown Copyright):
# http://www.education.gov.uk/schools/performance/download_data.html
# 
# Data used here in accordance with the DfE's terms:
# http://www.education.gov.uk/help/legalinformation/a005237/use-of-crown-copyright-material


import scraperwiki
import csv


# gives us a pretty screenshot
scraperwiki.scrape('http://www.finanstilsynet.dk/da/Tal-og-fakta/Virksomheder-under-tilsyn/VUT-soegning.aspx?aid=8')

# handy variables
base_url  = 'http://www.finanstilsynet.dk/da/Tal-og-fakta/Virksomheder-under-tilsyn/VUT-soegning.aspx?aid=8'

spine_csv = '' # selskabsnavn


