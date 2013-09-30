import scraperwiki
import mechanize
from bs4 import BeautifulSoup

#br = mechanize.Browser()

#url = 'http://namenlijst.rechtspraak.nl/'

#response = br.open(url)

#br.select_form("aspnetForm")    

#control = br.form.find_control("ctl00$ContentPlaceHolder1$chklInstances$0")

#response = br.submit()
#print response.read()
#br.back()   # go back
 
browser.open('namenlijst.rechtspraak.nl')
browser.select_form(name='aspnetForm')
browser['ctl00$ContentPlaceHolder1$chklInstances$0'] = 'Hoge Raad'
browser.submit()

soup = BeautifulSoup(browser.response().read())
 
body_tag = soup.body
all_paragraphs = soup.find_all('p')

print all_paragraphsimport scraperwiki
import mechanize
from bs4 import BeautifulSoup

#br = mechanize.Browser()

#url = 'http://namenlijst.rechtspraak.nl/'

#response = br.open(url)

#br.select_form("aspnetForm")    

#control = br.form.find_control("ctl00$ContentPlaceHolder1$chklInstances$0")

#response = br.submit()
#print response.read()
#br.back()   # go back
 
browser.open('namenlijst.rechtspraak.nl')
browser.select_form(name='aspnetForm')
browser['ctl00$ContentPlaceHolder1$chklInstances$0'] = 'Hoge Raad'
browser.submit()

soup = BeautifulSoup(browser.response().read())
 
body_tag = soup.body
all_paragraphs = soup.find_all('p')

print all_paragraphs