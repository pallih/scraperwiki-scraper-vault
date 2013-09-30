import scraperwiki
import urlparse
import lxml.html

#retrieve data from the journal details page
def scrape_journal_details(url, record):
    tree = lxml.html.parse(url, lxml.html.HTMLParser(encoding="utf-8"))
    subjectArea = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[2]/a[@title='view journal rank from this subject area']/text()")
    if len(subjectArea) > 0:
        record['SubjectArea'] = subjectArea[0].strip()

    subjectCategory = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[3]/a[@title='view journal rank from this subject category']/text()")
    if len(subjectCategory) > 0:
        record['SubjectCategory'] = subjectCategory[0].strip()

    publisher = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/a[starts-with(@title,'view all publisher')]/text()")
    if len(publisher) > 0:
        record['Publisher'] = publisher[0].strip()

    publicationType = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/text()")
    if len(publicationType) > 2:
        record['PublicationType'] = publicationType[2].strip()

    issn = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/text()")
    if len(issn) > 3:
        record['ISSN'] = issn[3].strip()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.tabla_datos tr")  # selects all <tr> blocks within <table class="tabla_datos">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['Nr'] = table_cells[0].text.strip()
            record['Title'] = row.cssselect("td.tit a")[0].text.strip()
            record['JournalDetailURL'] = row.cssselect("td.tit a")[0].attrib['href'].strip()
            journalURL = urlparse.urljoin(base_url, record['JournalDetailURL'])
            scrape_journal_details(journalURL, record)

            # Print out the data we've gathered
            print record
            # Finally, save the record to the datastore - 'Nr' is our unique key
            scraperwiki.sqlite.save(["Nr"], record)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    tree = lxml.html.parse(url, lxml.html.HTMLParser(encoding="utf-8"))
    next_link = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[3]/a[text()='Next >']/@href")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0])
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.scimagojr.com/'
starting_url = urlparse.urljoin(base_url, 'journalrank.php?category=0&area=0&year=2011&country=&order=sjr&min=0&min_type=cd&page=391')
scrape_and_look_for_next_link(starting_url)
import scraperwiki
import urlparse
import lxml.html

#retrieve data from the journal details page
def scrape_journal_details(url, record):
    tree = lxml.html.parse(url, lxml.html.HTMLParser(encoding="utf-8"))
    subjectArea = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[2]/a[@title='view journal rank from this subject area']/text()")
    if len(subjectArea) > 0:
        record['SubjectArea'] = subjectArea[0].strip()

    subjectCategory = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[3]/a[@title='view journal rank from this subject category']/text()")
    if len(subjectCategory) > 0:
        record['SubjectCategory'] = subjectCategory[0].strip()

    publisher = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/a[starts-with(@title,'view all publisher')]/text()")
    if len(publisher) > 0:
        record['Publisher'] = publisher[0].strip()

    publicationType = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/text()")
    if len(publicationType) > 2:
        record['PublicationType'] = publicationType[2].strip()

    issn = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[4]/text()")
    if len(issn) > 3:
        record['ISSN'] = issn[3].strip()

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root):
    rows = root.cssselect("table.tabla_datos tr")  # selects all <tr> blocks within <table class="tabla_datos">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['Nr'] = table_cells[0].text.strip()
            record['Title'] = row.cssselect("td.tit a")[0].text.strip()
            record['JournalDetailURL'] = row.cssselect("td.tit a")[0].attrib['href'].strip()
            journalURL = urlparse.urljoin(base_url, record['JournalDetailURL'])
            scrape_journal_details(journalURL, record)

            # Print out the data we've gathered
            print record
            # Finally, save the record to the datastore - 'Nr' is our unique key
            scraperwiki.sqlite.save(["Nr"], record)

# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_table(root)
    tree = lxml.html.parse(url, lxml.html.HTMLParser(encoding="utf-8"))
    next_link = tree.xpath("/html/body/div[@id='contenedor']/div[@id='subcontenedor']/div[@id='derecha']/div[@id='derecha_contenido']/p[3]/a[text()='Next >']/@href")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0])
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.scimagojr.com/'
starting_url = urlparse.urljoin(base_url, 'journalrank.php?category=0&area=0&year=2011&country=&order=sjr&min=0&min_type=cd&page=391')
scrape_and_look_for_next_link(starting_url)
