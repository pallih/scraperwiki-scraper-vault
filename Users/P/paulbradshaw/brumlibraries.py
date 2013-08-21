import scraperwiki
import re
import urlparse

    
url = 'http://birmingham.gov.uk/cs/Satellite?c=Page&childpagename=Lib-Community/PageLayout&cid=1223092582849&pagename=BCC/Common/Wrapper/Wrapper'
brumlibraries = scraperwiki.scrape(url)
print brumlibraries

#<a title="Castle Vale Library" href="/cs/Satellite?c=Page&amp;childpagename=Lib-Castle-Vale%2FPageLayout&amp;cid=1223104729461&amp;pagename=BCC%2FCommon%2FWrapper%2FWrapper"><strong>Castle Vale Library</strong></a>, Spitfire House, 10 High Street, Castle Vale, B35 7PR Tel: 0121 464 7335<br> 

entries = re.findall('<a.*?href="(.*?)">\s*<strong>(.*?)</strong>\s*</a>(.*?)<', brumlibraries)
for link, library, roughaddress in entries:
    lurl = urlparse.urljoin(url, re.sub("&amp;", "&", link))
    postcode = scraperwiki.geo.extract_gb_postcode(roughaddress)
    library = re.sub("<.*?>", " ", library)
    print postcode, library, lurl
    scraperwiki.datastore.save(["message"], {"message":library, "url":url}, latlng=scraperwiki.geo.gb_postcode_to_latlng(postcode))
import scraperwiki
import re
import urlparse

    
url = 'http://birmingham.gov.uk/cs/Satellite?c=Page&childpagename=Lib-Community/PageLayout&cid=1223092582849&pagename=BCC/Common/Wrapper/Wrapper'
brumlibraries = scraperwiki.scrape(url)
print brumlibraries

#<a title="Castle Vale Library" href="/cs/Satellite?c=Page&amp;childpagename=Lib-Castle-Vale%2FPageLayout&amp;cid=1223104729461&amp;pagename=BCC%2FCommon%2FWrapper%2FWrapper"><strong>Castle Vale Library</strong></a>, Spitfire House, 10 High Street, Castle Vale, B35 7PR Tel: 0121 464 7335<br> 

entries = re.findall('<a.*?href="(.*?)">\s*<strong>(.*?)</strong>\s*</a>(.*?)<', brumlibraries)
for link, library, roughaddress in entries:
    lurl = urlparse.urljoin(url, re.sub("&amp;", "&", link))
    postcode = scraperwiki.geo.extract_gb_postcode(roughaddress)
    library = re.sub("<.*?>", " ", library)
    print postcode, library, lurl
    scraperwiki.datastore.save(["message"], {"message":library, "url":url}, latlng=scraperwiki.geo.gb_postcode_to_latlng(postcode))
