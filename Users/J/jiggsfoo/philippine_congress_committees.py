import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import base64

# retrieve list page
list_url = 'http://www.congress.gov.ph/members/'
list_html = scraperwiki.scrape(list_url)
list_soup = BeautifulSoup(list_html)

def process_committees(website_id):
    profile_url = 'http://www.congress.gov.ph/members/search.php?congress=15&id=' + website_id
    profile_html = scraperwiki.scrape(profile_url)
    profile_soup = BeautifulSoup(profile_html)
    
    for section in profile_soup('div', 'col_hdr_2'):
        # save committee membership
        if (section.string.find('Committee Membership') >= 0):
            for committee in section.parent('div','p_bordered'):
                try: # if you can't find a committee...
                    committee_name = committee.a.string
                except AttributeError:
                    break                  

                try: # if you can't find a link, exit...
                    committee_id = committee.a['href'].split('id=')[1]
                except Exception:
                    break
                
                try: # if you cannot find a committee position, just make this blank
                    committee_pos = committee('span','sm_font')[0].string
                except Exception:
                    committee_pos = None

                # prepare committee data
                committee_data = {
                    "committee_id":committee_id,
                    "committee_name":committee_name
                }
                # save to database
                scraperwiki.sqlite.save(unique_keys=["committee_id"], data=committee_data, table_name="congcommittees")
                # prepare member committee data
                data = {
                    "website_id":website_id,
                    "committee_id":committee_id,
                    "committee_pos":committee_pos
                }
                # save to database
                scraperwiki.sqlite.save(unique_keys=["website_id","committee_id"], data=data, table_name="congcommitteesmembership")


for alist in list_soup('ul', id="nostylelist"):
    for item in alist('li'):
        website_id = item.a['href'].split('id=')[1]
        process_committees(website_id)

