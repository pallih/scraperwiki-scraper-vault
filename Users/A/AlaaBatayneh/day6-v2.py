import scraperwiki
from bs4 import BeautifulSoup

scraperwiki.sqlite.attach('dod-contracts-html')
scrapings = scraperwiki.sqlite.select("* from `dod-contracts-html`.swdata")

for scraping in scrapings:
    html = scraping['html']
    url = scraping['url']
    soup = BeautifulSoup(html)
    label_check = soup.findAll("span", "fieldrender-label")

    for label in label_check:
        title = soup.find("h2", "legend-edit").get_text()
        title = title.replace("English", "").strip()
        # Get the reference number
        if label.get_text().strip() == 'Reference number:':
            parent_ref = label.parent.get_text()
            reference = parent_ref.replace("Reference number:", "").strip()
        # Get length of contract
        elif label.get_text().strip() == 'Estimated length of contract:':
            parent_length = label.parent.get_text()
            length = parent_length.replace("Estimated length of contract:", "").strip()
        # Get award value
        elif label.get_text().strip() == 'Awarded value':
            parent_award = label.parent.get_text()
            award = parent_award.replace("Awarded value", "").strip()
        # Get location value
        elif label.get_text().strip() == 'Location where the contract is to be carried out:':
            parent_location = label.parent.get_text()
            location = parent_location.replace("Location where the contract is to be carried out:", "").strip()
        # Get organisation value
        elif label.get_text().strip() == 'Name of the buying organisation:':
            parent_organisation = label.parent.get_text()
            organisation = parent_organisation.replace("Name of the buying organisation:", "").strip()
            organisation = organisation.replace("English", "")
    data = {"url": url, "title": title, "reference" : reference, "length" : length, "award": award, "location" : location, "organisation": organisation }   
    scraperwiki.sqlite.save(["url"], data)

