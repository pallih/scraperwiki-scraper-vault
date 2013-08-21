"""

Number of Teachers and Administrators in California by Ethnicity,
detailed by County.

Fields (each category has a count and percentage measurement):
    year
    job
    county
    native_ct - American Indian/Alaskan Native
    native_pctg
    asian_ct
    asian_pctg
    islander_ct - Pacific Islander (counted as Asian before 1985)
    islander_pctg
    filipino_ct
    filipino_pctg
    hispanic_ct
    hispanic_pctg
    black_ct - Black, not Hispanic
    black_pctg
    white_ct - White, not hispanic
    white_pctg
    multiple_ct - Multiple/No Response
    multiple_pctg
    total

Modifications by <toqueteos>:
    - Fixed indentation
    - Changed single quotes to double ones, to be consistent
    - Updated scraperwiki data methods for data storage
    - Added a couple of changes to string concatenations, used string
        formatting instead. Check the docs!

"""

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

# Retrieve a page
years = [81, 90, 92, 93, 94, 95, 96]
jobs = ["tea", "admin"]
for k in years:
    for j in jobs:
        if j == "admin" and k == 90:
            continue
        
        # Use string formatting ;)
        # starting_url = "http://www.cde.ca.gov/ds/sd/dr/"+j+"eth"+str(k)+"c.asp"
        starting_url = "http://www.cde.ca.gov/ds/sd/dr/%seth%sc.asp" % (j, k)

        html = scraperwiki.scrape(starting_url)
        print html

        soup = BeautifulSoup(html)
        div = soup.find("div", {"id": "content"})
        table = div.find("table")

        rows = table.findAll("tr")

        for row in rows[1:]:

            vect = []
            cells = row.findAll("td")

            k2 = k+1

            # Use string formatting ;)
            # year = "19"+str(k)+"-19"+str(k2)
            year = "19%s-19%s" % (k, k2)

            if j == "admin":
                job = "administrator"
            else:
                job = "teacher"

            if k > 81:
                record = {
                    "year" : year,
                    "job" : job,
                    "county" : cells[0].text,
                    "native_ct" : cells[1].text,
                    "native_pctg" : cells[2].text,
                    "asian_ct" : cells[3].text,
                    "asian_pctg" : cells[4].text,
                    "islander_ct" : cells[5].text,
                    "islander_pctg" : cells[6].text,
                    "filipino_ct" : cells[7].text,
                    "filipino_pctg" : cells[8].text,
                    "hispanic_ct" : cells[9].text,
                    "hispanic_pctg" : cells[10].text,
                    "black_ct" : cells[11].text,
                    "black_pctg" : cells[12].text,
                    "white_ct" : cells[13].text,
                    "white_pctg" : cells[14].text,
                    "total" : cells[15].text,
                }
            else:
                record = {
                    "year" : year,
                    "job" : job,
                    "county" : cells[0].text,
                    "native_ct" : cells[1].text,
                    "native_pctg" : cells[2].text,
                    "asian_ct" : cells[3].text,
                    "asian_pctg" : cells[4].text,
                    "filipino_ct" : cells[5].text,
                    "filipino_pctg" : cells[6].text,
                    "hispanic_ct" : cells[7].text,
                    "hispanic_pctg" : cells[8].text,
                    "black_ct" : cells[9].text,
                    "black_pctg" : cells[10].text,
                    "white_ct" : cells[11].text,
                    "white_pctg" : cells[12].text,
                    "total" : cells[13].text,
                }

            # "datastore" is deprecated use "sqlite" instead
            scraperwiki.sqlite.save(["year","job","county"], record)
