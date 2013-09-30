###############################################################################
# Ontario MPP Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def scrape_contact_details(soup, record):
    for contact_details in soup.findAll("div", "mppcontact"):
        data = {}
        category = contact_details.find("div", "name").text.replace("&nbsp;", "").replace("'", "").replace(" ", "_").strip()
        for br in contact_details.find("div", "address").findAll("br"):
            br.replaceWith("\n")
        data["Address"] = contact_details.find("div", "address").text.split("\n")
        phone_numbers = contact_details.findAll("div", "phone")
        data["Telephone"] = phone_numbers[0].text.strip() if len(phone_numbers) > 0 else ""
        data["Fax"] = phone_numbers[1].text.strip() if len(phone_numbers) > 1 else ""
        record[category] = data

def scrape_mpp(id, record):
    record["URL"] = "http://www.ontla.on.ca/web/members/members_detail.do?locale=en&ID=" + id
    soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))
    img = soup.find("img", "mppimg")
    record["Image"] = "http://www.ontla.on.ca" + img["src"].strip() if img else ""
    email = soup.find("div", "email")
    record["Email"] = email.text.strip() if email else ""
    scrape_contact_details(soup, record)    

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    return name_parts[1].strip() + ' ' + name_parts[0].strip()    
    
# retrieve the list of current MPPs
starting_url = 'http://www.ontla.on.ca/web/members/members_current.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# iterate through each row in the table and extract the MPP data
table = soup.find("div", "tablebody").find('table')
rows = table.findAll("tr")
for row in rows:
    id = re.search("^MemberID(\d+)", row["id"]).group(1).strip()
    name = reorder_name(row.find("td", "mppcell").text)
    riding = row.find("td", "ridingcell").text
    riding = riding .replace("&nbsp;", " ").replace("--", "-").strip()
    record = { "ID" : id, "Name" : name, "Riding" : riding }
    # follow the link to each MPPs profile and scrape the data
    scrape_mpp(id, record)
    # save records to the datastore
    scraperwiki.sqlite.save(["ID"], record) 
    ###############################################################################
# Ontario MPP Scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup

def scrape_contact_details(soup, record):
    for contact_details in soup.findAll("div", "mppcontact"):
        data = {}
        category = contact_details.find("div", "name").text.replace("&nbsp;", "").replace("'", "").replace(" ", "_").strip()
        for br in contact_details.find("div", "address").findAll("br"):
            br.replaceWith("\n")
        data["Address"] = contact_details.find("div", "address").text.split("\n")
        phone_numbers = contact_details.findAll("div", "phone")
        data["Telephone"] = phone_numbers[0].text.strip() if len(phone_numbers) > 0 else ""
        data["Fax"] = phone_numbers[1].text.strip() if len(phone_numbers) > 1 else ""
        record[category] = data

def scrape_mpp(id, record):
    record["URL"] = "http://www.ontla.on.ca/web/members/members_detail.do?locale=en&ID=" + id
    soup = BeautifulSoup(scraperwiki.scrape(record["URL"]))
    img = soup.find("img", "mppimg")
    record["Image"] = "http://www.ontla.on.ca" + img["src"].strip() if img else ""
    email = soup.find("div", "email")
    record["Email"] = email.text.strip() if email else ""
    scrape_contact_details(soup, record)    

def reorder_name(name):
    name = name.replace("&nbsp;", " ")
    name_parts = name.split(",")
    return name_parts[1].strip() + ' ' + name_parts[0].strip()    
    
# retrieve the list of current MPPs
starting_url = 'http://www.ontla.on.ca/web/members/members_current.do'
html = scraperwiki.scrape(starting_url)
soup = BeautifulSoup(html)

# iterate through each row in the table and extract the MPP data
table = soup.find("div", "tablebody").find('table')
rows = table.findAll("tr")
for row in rows:
    id = re.search("^MemberID(\d+)", row["id"]).group(1).strip()
    name = reorder_name(row.find("td", "mppcell").text)
    riding = row.find("td", "ridingcell").text
    riding = riding .replace("&nbsp;", " ").replace("--", "-").strip()
    record = { "ID" : id, "Name" : name, "Riding" : riding }
    # follow the link to each MPPs profile and scrape the data
    scrape_mpp(id, record)
    # save records to the datastore
    scraperwiki.sqlite.save(["ID"], record) 
    