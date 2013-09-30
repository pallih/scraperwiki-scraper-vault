import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html
import mechanize

url = "http://www.lavaplace.com/"
username = ''
password = ''

br = mechanize.Browser()
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(url)

br.select_form("")

username_control = br.form.find_control(type="text")
password_control = br.form.find_control(type="password")
username_control.value = username
password_control.value = password

response = br.submit()
print response

exit()

for wurl in urls:
    curr_url = wurl 
    page_idx = 1
    
    while page_idx <= max_pages :
        error = True
        while error:
            try:
                html = scraperwiki.scrape(curr_url)
                root = lxml.html.fromstring(html)

                for tr in root.cssselect("div[class='ititle'] a"):    
                    url = tr.get("href")
                    html = scraperwiki.scrape(url)  
                    print html              
                    if html.find("age") != -1 :
                        print 'yo'
                        root2 = lxml.html.fromstring(html)
                        for mname in root2.cssselect("span[class='mbg-nw']"):
                            data = {
                                'url': url,
                                'merchant_name': mname.text
                            }
                            scraperwiki.sqlite.save(unique_keys=['url'],data=data)
    
                for next_page in root.cssselect("td[class='botpg-next'] a"):
                    print curr_url 
                    curr_url = next_page.get("href")
                    page_idx = page_idx +1             

                error = False
            except:
                print 'error'
                error = True
import scraperwiki

# Blank Python

import scraperwiki           
import lxml.html
import mechanize

url = "http://www.lavaplace.com/"
username = ''
password = ''

br = mechanize.Browser()
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

response = br.open(url)

br.select_form("")

username_control = br.form.find_control(type="text")
password_control = br.form.find_control(type="password")
username_control.value = username
password_control.value = password

response = br.submit()
print response

exit()

for wurl in urls:
    curr_url = wurl 
    page_idx = 1
    
    while page_idx <= max_pages :
        error = True
        while error:
            try:
                html = scraperwiki.scrape(curr_url)
                root = lxml.html.fromstring(html)

                for tr in root.cssselect("div[class='ititle'] a"):    
                    url = tr.get("href")
                    html = scraperwiki.scrape(url)  
                    print html              
                    if html.find("age") != -1 :
                        print 'yo'
                        root2 = lxml.html.fromstring(html)
                        for mname in root2.cssselect("span[class='mbg-nw']"):
                            data = {
                                'url': url,
                                'merchant_name': mname.text
                            }
                            scraperwiki.sqlite.save(unique_keys=['url'],data=data)
    
                for next_page in root.cssselect("td[class='botpg-next'] a"):
                    print curr_url 
                    curr_url = next_page.get("href")
                    page_idx = page_idx +1             

                error = False
            except:
                print 'error'
                error = True
