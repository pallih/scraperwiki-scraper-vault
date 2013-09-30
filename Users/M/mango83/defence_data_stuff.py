import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

    reference_number = soup.find("notice-header-details", "inner maintext")
    #print reference_number

ps = soup.find_all("p", "clearfix")

for p in ps:
    span = p.find("span")
    span_text = span.get_text().strip
    print span_text

"""p class="clearfix">
        <span class="inline fieldrender-label">
            Reference number:
        </span>
            MedGS/SVO/1611
      
    </p>"""



import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach("defence-contracts-all")

scrapings = scraperwiki.sqlite.select("* from 'defence-contracts-all'.swdata")

for scraping in scrapings:
    url = scraping["URL"]
    #print url

    soup = BeautifulSoup(scraping["HTML"])

    title = soup.find("div", "fieldset-title corners-top").get_text().replace("English", "").strip()
    #print title

    reference_number = soup.find("notice-header-details", "inner maintext")
    #print reference_number

ps = soup.find_all("p", "clearfix")

for p in ps:
    span = p.find("span")
    span_text = span.get_text().strip
    print span_text

"""p class="clearfix">
        <span class="inline fieldrender-label">
            Reference number:
        </span>
            MedGS/SVO/1611
      
    </p>"""



