import scraperwiki
import requests
from bs4 import BeautifulSoup

root_url = "http://www.denvergov.org"
main_page = "/streetclosures"
xpath = '//*[@id="dnn_ctr499298_HtmlModule_lblContent"]/strong/a'
closures_page = requests.get(root_url + main_page)

soup = BeautifulSoup(closures_page.text)
link = soup.find(id='dnn_ctr499298_HtmlModule_lblContent').find('a').get('href')

print linkimport scraperwiki
import requests
from bs4 import BeautifulSoup

root_url = "http://www.denvergov.org"
main_page = "/streetclosures"
xpath = '//*[@id="dnn_ctr499298_HtmlModule_lblContent"]/strong/a'
closures_page = requests.get(root_url + main_page)

soup = BeautifulSoup(closures_page.text)
link = soup.find(id='dnn_ctr499298_HtmlModule_lblContent').find('a').get('href')

print link