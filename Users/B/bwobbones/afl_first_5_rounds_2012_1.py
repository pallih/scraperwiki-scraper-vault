import scraperwiki
import lxml.html
import mechanize

br = mechanize.Browser()
#br.set_all_readonly(False)    
#br.set_handle_robots(False)  
#br.set_handle_refresh(False)  
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "http://www.tvtorrents.com"

response = br.open(url)

main = None

print response.read()

for form in br.forms():

    br.form = list(br.forms())[0]

    username = br.form.find_control("username")
    username.value = "bwobbones"
    pwd = br.form.find_control("password")
    pwd.value = "eeee"
    
    response = br.submit()
    main = response.read()

root = lxml.html.fromstring(main)

for option in root.cssselect(row):




import scraperwiki
import lxml.html
import mechanize

br = mechanize.Browser()
#br.set_all_readonly(False)    
#br.set_handle_robots(False)  
#br.set_handle_refresh(False)  
#br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = "http://www.tvtorrents.com"

response = br.open(url)

main = None

print response.read()

for form in br.forms():

    br.form = list(br.forms())[0]

    username = br.form.find_control("username")
    username.value = "bwobbones"
    pwd = br.form.find_control("password")
    pwd.value = "eeee"
    
    response = br.submit()
    main = response.read()

root = lxml.html.fromstring(main)

for option in root.cssselect(row):




