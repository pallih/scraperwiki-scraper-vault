import sys, time, os
from mechanize import Browser
import scraperwiki
import urlparse
import lxml.html

br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
i = 0
global_list =[]

for num in range(1,47):
    br.open("http://www.organic-bio.com/en/advanced-search2/?page={0}&country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0".format(num))
    
    
    nice_links = [l for l in br.links()
        if 'company' in l.url]
    
    global_list.extend(nice_links)

    record = {}
    for link in nice_links:

        i=i+1
        record['id'] = i
        record['url'] = link.url
        scraperwiki.sqlite.save(["id"], record)import sys, time, os
from mechanize import Browser
import scraperwiki
import urlparse
import lxml.html

br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
i = 0
global_list =[]

for num in range(1,47):
    br.open("http://www.organic-bio.com/en/advanced-search2/?page={0}&country=174&prgrp2=0&prodgrp2=0&prgrp3=0&prodgrp3=0&name=&city=&contact=&certification=0&service=0&fair=0".format(num))
    
    
    nice_links = [l for l in br.links()
        if 'company' in l.url]
    
    global_list.extend(nice_links)

    record = {}
    for link in nice_links:

        i=i+1
        record['id'] = i
        record['url'] = link.url
        scraperwiki.sqlite.save(["id"], record)