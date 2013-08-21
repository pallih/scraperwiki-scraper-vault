from dateutil import parser as dtparser
import lxml.html
import requests
import scraperwiki
import string
from urlparse import parse_qs, urlsplit, urlunsplit
from urllib import urlencode

"""
Pima County Food Safety Evaluation Ratings
By Name
http://www.pimahealth.org/restaurants/ratings/restname_alpha.asp?letter=A&Size=100&Submit=Submit

url args:
:letter: First letter of the restaurant name
:size: Number of results per page
:page: Page number of results

-------------------------------------------------------------------------------
By Rating
http://www.pimahealth.org/restaurants/ratings/restrate_alpha.asp

e.g.
http://www.pimahealth.org/restaurants/ratings/restrate_alpha.asp?letter=N&Size=30&monthin=11&yearin=2012
url args:
:letter: string, Letter grade, one of:

E = (Excellent) No critical violations noted at time of inspection.
G = (Good) Critical violation(s) noted and corrected prior to the completion of the inspection.
N = (Needs Improvement) Critical violation(s) noted at the time of inspection, but not able to correct prior to the completion of the inspection. Violation(s) were followed up within a ten day period to ensure compliance.
P = (Provisional License) Five or more critical violations noted at time of inspection. Establishment must be re-inspected within ten days.

:size: integer, number of results per page
:monthin: integer, Month
:yearin: integer, Year
"""
base_url = 'http://www.pimahealth.org/restaurants/ratings/restname_alpha.asp'
base_query = dict(
    letter='A',
    size=10000,
    page=1,
    submit='Submit'
)
scheme, netloc, path, query, fragment = urlsplit(base_url)
# xpath queries
qry_rows = '//table[@id="ratingtable"]//td/span[@class="tabledata"][1]/../..'
qry_lastpage = '//table[@id="ratingtable"]//span[@class="pagebreadcrumb"]//u[text()="Last Page"]/../..'


def update_url(querydict=None):
    """
    Return a complete url given a dictionary of querystring args
    """
    if querydict is None:
        querydict = {}
    for k,v in querydict.items():
        base_query[k] = v
    query = urlencode(base_query)
    return urlunsplit((scheme, netloc, path, query, fragment))


def extract_ratings(tr):
    """
    Extract name, street_address, inspection_date, grade from an Element row
    :return: dict
    """
    elName, elAddress, elDate, elGrade = tr.findall('td')
    nameEls = list(elName.iterdescendants('span'))
    #namedesc = ''.join([span.text for span in elName.iterdescendants('span')])

    incident_id = extract_incident_id(nameEls[0])
    #if incident_id is not None:
    #    print("Incident %s found" % (incident_id,))

    address = ''.join([span.text for span in elAddress.iterdescendants('span')])
    date = ''.join([span.text for span in elDate.iterdescendants('span')])
    date = dtparser.parse(date)
    grade = ''.join([span.text for span in elGrade.iterdescendants('span')])
    results = dict(
        name=nameEls[0].text,
        street_address=address,
        inspection_date=date,
        grade=grade
    )
    return results


def extract_incident_id(el):
    """
    Extract the incident ID for rows where the name is wrapped in an anchor
    Anchor href contains a query argument of InsId
    :param el: Element object
    """
    parent = el.getparent()
    if parent.tag == 'a':
        href = parent.get('href')
        try:
            qwargs = parse_qs(urlsplit(href).query)
        except AttributeError:
            return None
        else:
            return qwargs.get('InsId', None)


def extract_last_page(el):
    """
    If pagination exists, extract the last page
    :returns: number of pages
    """
    # Extract the last page if there is pagination
    results = root.xpath(qry_lastpage)
    pages = 1
    if len(results) > 0:
        href = results[0].get('href')
        parsed = parse_qs(urlsplit(href).query)
        pages = parsed.get('PAGE', ['1'])[0]
        try:
            pages = int(pages)
        except ValueError:
            pages = 1
    return pages


url = update_url()
urls = [url]
data = []

for letter in string.uppercase:
    url = update_url({'letter': letter})

    # Initial dataset, may be paginated
    retries = 3
    while retries:
        try:
            html = requests.get(url).text
        except requests.ConnectionError, e:
            retries -= 1
            if retries:
                print("Error fetching letter {letter}...retry count: {retries}".format(letter=letter, retries=retries))
            else:
                print("Error fetching {url}...skipping {letter}\n{exc}".format(url=url, letter=letter, exc=e))
            continue
        else:
            retries = 0

    root = lxml.html.fromstring(html)
    # Build paginated querystring for each remaining page
    pages = extract_last_page(root)
    print('%d pages for letter %s' % (pages, letter))
    print("Processing page 1")
    for tr in root.xpath(qry_rows):
        data.append(extract_ratings(tr))

    for page in range(1, pages):
        print("Processing page {page} of letter {letter}".format(page=page + 1, letter=letter))
        url = update_url({'page': page})

        retries = 3
        while retries:
            try:
                html = requests.get(url).text
            except requests.ConnectionError, e:
                retries -= 1
                if retries:
                    print("Error fetching page {page} of letter {letter}...retry count: {retries}".format(page=page, letter=letter, retries=retries))
                else:
                    print("Error fetching {url}...skipping page {page} of letter {letter}\n{exc}".format(url=url, letter=letter, exc=e))
                continue
            else:
                retries = 0
        root = lxml.html.fromstring(html)
        for tr in root.xpath(qry_rows):
            data.append(extract_ratings(tr))

scraperwiki.sqlite.save(table_name='pimahealth_restaurant_ratings', unique_keys=['name', 'street_address', 'inspection_date'], data=data)
