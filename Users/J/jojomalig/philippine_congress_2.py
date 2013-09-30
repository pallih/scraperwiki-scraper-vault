import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import base64

# retrieve list page
list_url = 'http://www.congress.gov.ph/members/'
list_html = scraperwiki.scrape(list_url)
list_soup = BeautifulSoup(list_html)

def process_profile(website_id):
    profile_url = 'http://www.congress.gov.ph/members/search.php?congress=15&id=' + website_id
    profile_html = scraperwiki.scrape(profile_url)
    profile_soup = BeautifulSoup(profile_html)
    
    profile_pic_path = profile_soup('p','mem_info')[0].find('img')['src']
    # sometimes these causes a BadStatusLine error, so we need to handle it gracefully
    try:
        profile_pic = base64.b64encode(urllib2.urlopen(list_url + profile_pic_path).read())
    except Exception:
        profile_pic = None
    
    # remove email link for now when saving contact info
    try:
        profile_soup('p','mem_info')[0].find('a','sm_link').extract()
    except AttributeError:
        pass
    profile_contact = "\n".join(profile_soup('p','mem_info')[0].find('span','sm_font').renderContents().split('<br />'))
    
    # check if party list
    party_list = ''
    if (profile_soup('p','mem_info')[0].next.next == 'Sectoral Representative'):
        party_list = profile_soup('p','mem_info')[0].next.next.next.next
    
    return profile_pic_path, profile_pic, profile_contact, party_list



for alist in list_soup('ul', id="nostylelist"):
    for item in alist('li'):
        website_id = item.a['href'].split('id=')[1]
        rep_name = item.a.string.split(',')
        prov = ''
        dist = ''
        if (item.a['title'] != ''):
            prov = item.a['title'].split(',')[0]
            dist = item.a['title'].split(',')[1].strip()

        print "Processing " + rep_name[0] + ", " + rep_name[1] + "..."
        profile_pic_path, profile_pic, profile_contact, party_list = process_profile(website_id)
        
        # prepare data
        data = {
            "website_id":website_id,
            "first_name":rep_name[0],
            "last_name":rep_name[1].strip(),
            "province":prov,
            "district":dist,
            "profile_pic_path":profile_pic_path,
            "profile_pic":profile_pic,
            "profile_contact":profile_contact,
            "party_list":party_list
        }
        # save to member database
        scraperwiki.sqlite.save(unique_keys=["website_id"], data=data, table_name="congmembers")


# save committee info
scraperwiki.sqlite.attach("phililippine_congress_committees", "committees")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congcommittees`")
scraperwiki.sqlite.execute("CREATE TABLE `congcommittees` (`committee_name` text, `committee_id` text)")
scraperwiki.sqlite.execute("INSERT INTO `congcommittees` (`committee_name`, `committee_id`) SELECT `committee_name`, `committee_id` FROM `committees.congcommittees`")
scraperwiki.sqlite.commit()
# save committee membership info
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congcommitteesmembership`")
scraperwiki.sqlite.execute("CREATE TABLE `congcommitteesmembership` (`committee_pos` text, `website_id` text, `committee_id` text)")
scraperwiki.sqlite.execute("INSERT INTO `congcommitteesmembership` (`committee_pos`, `website_id`, `committee_id`) SELECT `committee_pos`, `website_id`, `committee_id` FROM `committees.congcommitteesmembership`")
scraperwiki.sqlite.commit()

# save bills info
scraperwiki.sqlite.attach("phililippine_congress_bills", "bills")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congbills`")
scraperwiki.sqlite.execute("CREATE TABLE `congbills` (`bill_no` text, `status` text, `title` text, `website_id` text, `history_link` text, `type` text)")
scraperwiki.sqlite.execute("INSERT INTO `congbills` (`bill_no`, `status`, `title`, `website_id`, `history_link`, `type`) SELECT `bill_no`, `status`, `title`, `website_id`, `history_link`, `type` FROM `bills.congbills`")
scraperwiki.sqlite.commit()
import scraperwiki
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import base64

# retrieve list page
list_url = 'http://www.congress.gov.ph/members/'
list_html = scraperwiki.scrape(list_url)
list_soup = BeautifulSoup(list_html)

def process_profile(website_id):
    profile_url = 'http://www.congress.gov.ph/members/search.php?congress=15&id=' + website_id
    profile_html = scraperwiki.scrape(profile_url)
    profile_soup = BeautifulSoup(profile_html)
    
    profile_pic_path = profile_soup('p','mem_info')[0].find('img')['src']
    # sometimes these causes a BadStatusLine error, so we need to handle it gracefully
    try:
        profile_pic = base64.b64encode(urllib2.urlopen(list_url + profile_pic_path).read())
    except Exception:
        profile_pic = None
    
    # remove email link for now when saving contact info
    try:
        profile_soup('p','mem_info')[0].find('a','sm_link').extract()
    except AttributeError:
        pass
    profile_contact = "\n".join(profile_soup('p','mem_info')[0].find('span','sm_font').renderContents().split('<br />'))
    
    # check if party list
    party_list = ''
    if (profile_soup('p','mem_info')[0].next.next == 'Sectoral Representative'):
        party_list = profile_soup('p','mem_info')[0].next.next.next.next
    
    return profile_pic_path, profile_pic, profile_contact, party_list



for alist in list_soup('ul', id="nostylelist"):
    for item in alist('li'):
        website_id = item.a['href'].split('id=')[1]
        rep_name = item.a.string.split(',')
        prov = ''
        dist = ''
        if (item.a['title'] != ''):
            prov = item.a['title'].split(',')[0]
            dist = item.a['title'].split(',')[1].strip()

        print "Processing " + rep_name[0] + ", " + rep_name[1] + "..."
        profile_pic_path, profile_pic, profile_contact, party_list = process_profile(website_id)
        
        # prepare data
        data = {
            "website_id":website_id,
            "first_name":rep_name[0],
            "last_name":rep_name[1].strip(),
            "province":prov,
            "district":dist,
            "profile_pic_path":profile_pic_path,
            "profile_pic":profile_pic,
            "profile_contact":profile_contact,
            "party_list":party_list
        }
        # save to member database
        scraperwiki.sqlite.save(unique_keys=["website_id"], data=data, table_name="congmembers")


# save committee info
scraperwiki.sqlite.attach("phililippine_congress_committees", "committees")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congcommittees`")
scraperwiki.sqlite.execute("CREATE TABLE `congcommittees` (`committee_name` text, `committee_id` text)")
scraperwiki.sqlite.execute("INSERT INTO `congcommittees` (`committee_name`, `committee_id`) SELECT `committee_name`, `committee_id` FROM `committees.congcommittees`")
scraperwiki.sqlite.commit()
# save committee membership info
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congcommitteesmembership`")
scraperwiki.sqlite.execute("CREATE TABLE `congcommitteesmembership` (`committee_pos` text, `website_id` text, `committee_id` text)")
scraperwiki.sqlite.execute("INSERT INTO `congcommitteesmembership` (`committee_pos`, `website_id`, `committee_id`) SELECT `committee_pos`, `website_id`, `committee_id` FROM `committees.congcommitteesmembership`")
scraperwiki.sqlite.commit()

# save bills info
scraperwiki.sqlite.attach("phililippine_congress_bills", "bills")
scraperwiki.sqlite.execute("DROP TABLE IF EXISTS `congbills`")
scraperwiki.sqlite.execute("CREATE TABLE `congbills` (`bill_no` text, `status` text, `title` text, `website_id` text, `history_link` text, `type` text)")
scraperwiki.sqlite.execute("INSERT INTO `congbills` (`bill_no`, `status`, `title`, `website_id`, `history_link`, `type`) SELECT `bill_no`, `status`, `title`, `website_id`, `history_link`, `type` FROM `bills.congbills`")
scraperwiki.sqlite.commit()
