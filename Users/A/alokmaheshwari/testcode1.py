import scraperwiki
import mechanize 
import lxml.html
import urllib,urllib2
import time


#Edit the exourl and siteurl as per your site

exourl = "http://syndication.exoclick.com/ads-iframe-display.php?type=300x250&login=xhamster&cat=2&search=&ad_title_color=0000cc&bgcolor=FFFFFF&border=0&border_color=000000&font=&block_keywords=&ad_text_color=000000&ad_durl_color=008000&adult=0&sub=0&text_only=0&show_thumb=0&idzone=100633&idsite=34954"

siteurl = "http://xhamster.com"




#The magic begins here

ad_url=exourl+"&p="+siteurl+"&dt="+str(time.time()*1000);

print  ad_url

# So we have to do with shady CGI proxies on port 80
# If these break, get new ones from:
# http://www.publicproxyservers.com/proxy/list_uptime1.html

#eu_proxy = 'http://2bgoodproxy.uk.tc/browse.php?u=%s'
#eu_proxy= 'http://www.headproxy.com/browse.php?u=%s'
#us_proxy = 'http://alivebyspeed.info/browse.php?u=%s' 

#req = urllib2.Request(eu_proxy % urllib.quote(ad_url))
#req.add_header('Referer', eu_proxy % '') # These proxies need Referer header
#html = urllib2.urlopen(req).read() 




html = scraperwiki.scrape(ad_url)
print html

import lxml.html
root = lxml.html.fromstring(html)

links= root.iterlinks()

for element, attribute, link, pos in root.iterlinks():
    if attribute == "href":
        #print link
        exo_url=link
    if attribute == "src":
        #print link
        image_url=link


print exo_url
print image_url



surl = exo_url+'&js=1'

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(True)  # can sometimes hang without this 
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 
br.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')]
 

response = br.open(surl)

print response.read()

br.form = list(br.forms())[0] 

response = br.submit()

lp_url= response.geturl() 

print  lp_url
#print response.read() 

#br.set_handle_refresh(True)  # can sometimes hang without this  

#response1 = br.response()  # get the response again
#print response1.read()     # can apply lxml.html.fromstring() 



scraperwiki.sqlite.save(unique_keys=["image"], data={"image":image_url,"lp_url":lp_url,"exourl":exo_url})


