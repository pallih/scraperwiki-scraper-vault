import scraperwiki
import mechanize
import string
import re
import itertools
from lxml import etree

pattern = re.compile("dgPublicRegistry[^']*")

start_url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
form_name = 'Form1'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def scrape_page(resp):
    doc = etree.HTML(resp.read())
    for tr in doc.xpath("//tr[@title='Please click for more information']"):
        try:
            last_name, given_name = tr.getchildren()
            scraperwiki.datastore.save(['last_name', 'given_name'], {'last_name': last_name.text, 'given_name': given_name.text})
        except:
            print "Failed to get name: ", tr.getchildren()

completed_letters = scraperwiki.metadata.get('completed_letters',[])
print completed_letters
        
for l in string.lowercase:
    if l in completed_letters:
        continue

    br.open(start_url)
    br.select_form(name=form_name)
    br.form['txtboxSurname'] = l
    req = br.form.click('btnSearch')
    scrape_page(br.open(req))
    
    for n in itertools.count(2):
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name=form_name)
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = pattern.findall(link.url)[0]
        br['__EVENTARGUMENT'] = ''
        br.submit()
        scrape_page(br.response())

    completed_letters.append(l)
    scraperwiki.metadata.save('completed_letters', completed_letters)

scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
import scraperwiki
import mechanize
import string
import re
import itertools
from lxml import etree

pattern = re.compile("dgPublicRegistry[^']*")

start_url = 'http://www.bcct.ca/MemberServices/FindATeacher.aspx'
form_name = 'Form1'

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

def scrape_page(resp):
    doc = etree.HTML(resp.read())
    for tr in doc.xpath("//tr[@title='Please click for more information']"):
        try:
            last_name, given_name = tr.getchildren()
            scraperwiki.datastore.save(['last_name', 'given_name'], {'last_name': last_name.text, 'given_name': given_name.text})
        except:
            print "Failed to get name: ", tr.getchildren()

completed_letters = scraperwiki.metadata.get('completed_letters',[])
print completed_letters
        
for l in string.lowercase:
    if l in completed_letters:
        continue

    br.open(start_url)
    br.select_form(name=form_name)
    br.form['txtboxSurname'] = l
    req = br.form.click('btnSearch')
    scrape_page(br.open(req))
    
    for n in itertools.count(2):
        try:
            link = br.find_link(text=str(n))
        except:
            try:
                link = br.find_link(text="[Next]")
            except:
                break

        br.select_form(name=form_name)
        br.form.set_all_readonly(False)
        br.form.find_control('nav:top_search_submit').disabled=True
        br['__EVENTTARGET'] = pattern.findall(link.url)[0]
        br['__EVENTARGUMENT'] = ''
        br.submit()
        scrape_page(br.response())

    completed_letters.append(l)
    scraperwiki.metadata.save('completed_letters', completed_letters)

scraperwiki.metadata.save('completed_letters', []) # Let's start again :)
