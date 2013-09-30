###############################################################################
# Scraper for Cheshire West and Chester Council
###############################################################################

import scraperwiki
import re
import urllib2
import mechanize
from BeautifulSoup import BeautifulSoup

base_url = "http://cmttpublic.cheshirewestandchester.gov.uk/"

index_url = base_url + "mgMemberIndex.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

base = br.open(index_url)

html = base.read()

sections = re.findall('(?si)<div  class="mgThumbsList" >\r\n\n<ul >\n\t\t\r\n\t(.*?)\n</ul>\n\r\n\t\t</div>', html)

councillors = re.findall('(?si)<li>(.*?)</li>', sections[0])

for councillor in councillors:
    data = {}
    
    councillor_uid = re.findall('(?si)<a  href="(.*?)"  >', councillor)
    
    link = base_url + councillor_uid[0]
    
    page = br.open(link)
    
    read_page = page.read()
    
    name = re.findall('(?si)<div id="maintitle"><div class="titletop"><div class="titlebot"><h1>(.*?)</h1></div></div></div>', read_page)
    print "NAME: ", unicode(name[0])
    data['name'] = unicode(name[0])
    
    party = re.findall('(?si)<p><span  class="mgLabel" >Party:&nbsp;</span>(.*?)</p>', read_page)
    data['party'] = unicode(party[0])
    
    ward = re.findall('(?si)<p><span  class="mgLabel" >Ward:&nbsp;</span>(.*?)</p>', read_page)
    data['ward'] = unicode(ward[0])
    
    title = re.findall('(?si)<p><span  class="mgLabel" >Title:&nbsp;</span>(.*?)</p>', read_page)
    if title:
        data['title'] = unicode(title[0])
        
    address = re.findall('(?si)<p><span  class="mgLabel" >Home Address:&nbsp;</span>(.*?)</p>', read_page)
    if address:
        address = re.sub("   \r\n\t\t\t<br />|\r\n\t\t|\r\n", "", address[0])
        address = re.sub("<br />", ", ", address)
        data['address'] = unicode(address)
    
    phone = re.findall('(?si)<p><span  class="mgLabel" >Phone:&nbsp;</span>(.*?)</p>', read_page)
    if phone:
        phone = re.sub(" |\r|\n|\t", "", phone[0])
        data['phone'] = unicode(phone)
    
    mobile = re.findall('(?si)<p><span  class="mgLabel" >Mobile:&nbsp;</span>(.*?)</p>', read_page)
    if mobile:
        mobile = re.sub(" |\r|\n|\t", "", mobile[0])
        data['mobile'] = unicode(mobile)
    
    business_phone = re.findall('(?si)<p><span  class="mgLabel" >Bus. Phone:&nbsp;</span>(.*?)</p>', read_page)
    if business_phone:
        business_phone = re.sub(" |\r|\n|\t", "", business_phone[0])
        data['business_phone'] = unicode(business_phone)

    business_fax = re.findall('(?si)<p><span  class="mgLabel" >Bus. Fax:&nbsp;</span>(.*?)</p>', read_page)
    if business_fax:
        business_fax = re.sub(" |\r|\n|\t", "", business_fax[0])
        data['business_fax'] = unicode(business_fax)
    
    business_email = re.findall('(?si)<a  href="mailto:(.*?)"  title=".*?">.*?</a>', read_page)
    if business_email:
        data['business_email'] = unicode(business_email[0])
    
    print "DATA: ", data
    scraperwiki.datastore.save(["name", "party"], data)
    print "-----------------------------------------------"
    br.back()###############################################################################
# Scraper for Cheshire West and Chester Council
###############################################################################

import scraperwiki
import re
import urllib2
import mechanize
from BeautifulSoup import BeautifulSoup

base_url = "http://cmttpublic.cheshirewestandchester.gov.uk/"

index_url = base_url + "mgMemberIndex.aspx"

br = mechanize.Browser()
br.set_handle_robots(False)

base = br.open(index_url)

html = base.read()

sections = re.findall('(?si)<div  class="mgThumbsList" >\r\n\n<ul >\n\t\t\r\n\t(.*?)\n</ul>\n\r\n\t\t</div>', html)

councillors = re.findall('(?si)<li>(.*?)</li>', sections[0])

for councillor in councillors:
    data = {}
    
    councillor_uid = re.findall('(?si)<a  href="(.*?)"  >', councillor)
    
    link = base_url + councillor_uid[0]
    
    page = br.open(link)
    
    read_page = page.read()
    
    name = re.findall('(?si)<div id="maintitle"><div class="titletop"><div class="titlebot"><h1>(.*?)</h1></div></div></div>', read_page)
    print "NAME: ", unicode(name[0])
    data['name'] = unicode(name[0])
    
    party = re.findall('(?si)<p><span  class="mgLabel" >Party:&nbsp;</span>(.*?)</p>', read_page)
    data['party'] = unicode(party[0])
    
    ward = re.findall('(?si)<p><span  class="mgLabel" >Ward:&nbsp;</span>(.*?)</p>', read_page)
    data['ward'] = unicode(ward[0])
    
    title = re.findall('(?si)<p><span  class="mgLabel" >Title:&nbsp;</span>(.*?)</p>', read_page)
    if title:
        data['title'] = unicode(title[0])
        
    address = re.findall('(?si)<p><span  class="mgLabel" >Home Address:&nbsp;</span>(.*?)</p>', read_page)
    if address:
        address = re.sub("   \r\n\t\t\t<br />|\r\n\t\t|\r\n", "", address[0])
        address = re.sub("<br />", ", ", address)
        data['address'] = unicode(address)
    
    phone = re.findall('(?si)<p><span  class="mgLabel" >Phone:&nbsp;</span>(.*?)</p>', read_page)
    if phone:
        phone = re.sub(" |\r|\n|\t", "", phone[0])
        data['phone'] = unicode(phone)
    
    mobile = re.findall('(?si)<p><span  class="mgLabel" >Mobile:&nbsp;</span>(.*?)</p>', read_page)
    if mobile:
        mobile = re.sub(" |\r|\n|\t", "", mobile[0])
        data['mobile'] = unicode(mobile)
    
    business_phone = re.findall('(?si)<p><span  class="mgLabel" >Bus. Phone:&nbsp;</span>(.*?)</p>', read_page)
    if business_phone:
        business_phone = re.sub(" |\r|\n|\t", "", business_phone[0])
        data['business_phone'] = unicode(business_phone)

    business_fax = re.findall('(?si)<p><span  class="mgLabel" >Bus. Fax:&nbsp;</span>(.*?)</p>', read_page)
    if business_fax:
        business_fax = re.sub(" |\r|\n|\t", "", business_fax[0])
        data['business_fax'] = unicode(business_fax)
    
    business_email = re.findall('(?si)<a  href="mailto:(.*?)"  title=".*?">.*?</a>', read_page)
    if business_email:
        data['business_email'] = unicode(business_email[0])
    
    print "DATA: ", data
    scraperwiki.datastore.save(["name", "party"], data)
    print "-----------------------------------------------"
    br.back()