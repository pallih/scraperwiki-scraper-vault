"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re
from bs4 import BeautifulSoup


# The URLs we're going to scrape:

urls = """

https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=12VI&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=26CC&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25GV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01IC&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01NJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=21CS&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=21CY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25EF&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=13US&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01OE&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=11UL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=14YD&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZV&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LR&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=08PG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04CY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LF&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PN&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27DV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PM&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LU&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28AY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=14NZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LT&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04FO&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28DE&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04EU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04EM&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25RA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PT&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27YU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LH&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=09MR&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28AX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=05EL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LP&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=00GT&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=20MQ&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LN&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25MA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27GZ&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25MB&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LV&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01AA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04NZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PN&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=23KG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PK&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=17WH&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02OV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=18XX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=30BC&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=05EA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=23JA&p_jaar=2012    




""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
#def gettext(html):

#  """Return the text within html, removing any HTML tags it contained."""
 # cleaned = re.sub('<.*?>', '', html)  # remove tags
 # cleaned = ' '.join(cleaned.split())  # collapse whitespace
 # return cleaned



for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        # re.DOTALL makes it work across multiple lines as well.
        
        naam = re.findall("<h1>(.*?)</h1>", page, re.DOTALL)
        financieeltoezicht = re.findall("toezicht:(.*?)</td>", page, re.DOTALL)

        soup = BeautifulSoup(page)


        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'financieeltoezicht': financieeltoezicht, 'naam': naam}

        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re
from bs4 import BeautifulSoup


# The URLs we're going to scrape:

urls = """

https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=12VI&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=26CC&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25GV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01IC&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01NJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=21CS&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=21CY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25EF&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=13US&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01OE&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=11UL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=14YD&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZV&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LR&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=08PG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04CY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=24ZZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LF&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PN&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27DV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PM&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LU&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28AY&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=14NZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LT&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04FO&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28DE&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04EU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04EM&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25RA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PT&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PJ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27YU&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LH&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=09MR&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=28AX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=05EL&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25PV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LP&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=00GT&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=20MQ&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LN&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25MA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=27GZ&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LW&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25MB&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=25LV&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=01AA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=04NZ&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PN&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=23KG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PK&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=17WH&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PG&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02OV&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=18XX&p_jaar=2012    
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=30BC&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=02PA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=05EA&p_jaar=2012
https://schooldossier.owinsp.nl/isd/ips.ips_pck_tonen.profiel?p_brin=23JA&p_jaar=2012    




""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
#def gettext(html):

#  """Return the text within html, removing any HTML tags it contained."""
 # cleaned = re.sub('<.*?>', '', html)  # remove tags
 # cleaned = ' '.join(cleaned.split())  # collapse whitespace
 # return cleaned



for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        # re.DOTALL makes it work across multiple lines as well.
        
        naam = re.findall("<h1>(.*?)</h1>", page, re.DOTALL)
        financieeltoezicht = re.findall("toezicht:(.*?)</td>", page, re.DOTALL)

        soup = BeautifulSoup(page)


        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'financieeltoezicht': financieeltoezicht, 'naam': naam}

        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url